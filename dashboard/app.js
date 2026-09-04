let streams = [];

let currentModalStream = null;


/* --------------------------------
   HELPERS
-------------------------------- */

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


function formatNumber(value) {
    return Number(value || 0).toLocaleString();
}


function formatUptime(seconds) {

    seconds = Math.max(
        0,
        Number(seconds || 0)
    );

    const days = Math.floor(
        seconds / 86400
    );

    seconds %= 86400;

    const hours = Math.floor(
        seconds / 3600
    );

    seconds %= 3600;

    const minutes = Math.floor(
        seconds / 60
    );

    const secs = Math.floor(
        seconds % 60
    );

    if (days > 0) {
        return `${days}d ${hours}h ${minutes}m`;
    }

    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    }

    if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    }

    return `${secs}s`;
}


function formatDuration(startedAt) {

    if (!startedAt) {
        return "00:00:00";
    }

    const start = new Date(startedAt).getTime();

    if (Number.isNaN(start)) {
        return "00:00:00";
    }

    const now = Date.now();

    let total = Math.max(
        0,
        Math.floor((now - start) / 1000)
    );

    const days = Math.floor(
        total / 86400
    );

    total %= 86400;

    const hours = Math.floor(
        total / 3600
    );

    total %= 3600;

    const minutes = Math.floor(
        total / 60
    );

    const seconds = total % 60;

    const hh = String(hours).padStart(2, "0");
    const mm = String(minutes).padStart(2, "0");
    const ss = String(seconds).padStart(2, "0");

    if (days > 0) {
        return `${days}d ${hh}:${mm}:${ss}`;
    }

    return `${hh}:${mm}:${ss}`;
}


function showToast(message) {

    const toast =
        document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2500);
}


async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            headers: {
                "Content-Type":
                    "application/json"
            },
            ...options
        }
    );

    let data = {};

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );
    }

    return data;
}


/* --------------------------------
   NAVIGATION
-------------------------------- */

function openPage(page) {

    document
        .querySelectorAll(".page")
        .forEach(element => {
            element.classList.remove("active");
        });

    document
        .querySelectorAll(".nav-item")
        .forEach(element => {
            element.classList.remove("active");
        });


    const pageElement =
        document.getElementById(
            `${page}Page`
        );

    if (pageElement) {
        pageElement.classList.add("active");
    }


    const nav =
        document.querySelector(
            `.nav-item[data-page="${page}"]`
        );

    if (nav) {
        nav.classList.add("active");
    }


    const names = {
        dashboard: "Dashboard",
        streams: "Live Streams",
        health: "Stream Health"
    };

    document.getElementById(
        "pageName"
    ).textContent =
        (names[page] || page).toUpperCase();

    document.getElementById(
        "pageTitle"
    ).textContent =
        names[page] || page;
}


document
    .querySelectorAll(
        "[data-page]"
    )
    .forEach(element => {

        element.addEventListener(
            "click",
            () => {

                openPage(
                    element.dataset.page
                );

            }
        );

    });


/* --------------------------------
   CREATE STREAM
-------------------------------- */

document
    .getElementById("createStreamForm")
    .addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            const name =
                document
                    .getElementById("streamName")
                    .value
                    .trim();

            const source =
                document
                    .getElementById("streamSource")
                    .value
                    .trim();

            if (!name) {
                showToast(
                    "Stream name is required"
                );

                return;
            }

            try {

                const data = await api(
                    "/api/streams",
                    {
                        method: "POST",

                        body: JSON.stringify({
                            name,
                            source
                        })
                    }
                );


                document
                    .getElementById(
                        "createStreamForm"
                    )
                    .reset();


                if (source) {

                    showToast(
                        "Stream created. Starting..."
                    );

                    await startStream(
                        data.id
                    );

                } else {

                    showToast(
                        "Scheduled stream created"
                    );

                }

                await loadStreams();

            } catch (error) {

                showToast(
                    error.message
                );

            }

        }
    );


/* --------------------------------
   STREAM ACTIONS
-------------------------------- */

async function startStream(streamId) {

    try {

        await api(
            `/api/streams/${streamId}/start`,
            {
                method: "POST"
            }
        );

        showToast(
            "Stream started"
        );

        await loadStreams();

    } catch (error) {

        showToast(
            error.message
        );

    }
}


async function stopStream(streamId) {

    const stream =
        streams.find(
            item => item.id === streamId
        );

    const name =
        stream?.name ||
        "this stream";

    const confirmed =
        window.confirm(
            `Stop "${name}"?\n\nThis will kill FFmpeg, delete the HLS files and remove the stream from the server.`
        );

    if (!confirmed) {
        return;
    }


    try {

        await api(
            `/api/streams/${streamId}/stop`,
            {
                method: "POST"
            }
        );

        showToast(
            "Stream stopped and removed"
        );

        await loadStreams();

    } catch (error) {

        showToast(
            error.message
        );

    }
}


async function copyM3u8(streamId) {

    const stream =
        streams.find(
            item => item.id === streamId
        );

    if (!stream) {
        return;
    }

    if (!stream.running) {

        showToast(
            "Stream is not currently live"
        );

        return;
    }


    const url =
        `${window.location.origin}/hls/${stream.id}/index.m3u8`;


    try {

        await navigator.clipboard.writeText(
            url
        );

        showToast(
            "M3U8 link copied"
        );

    } catch {

        showToast(
            "Could not copy link"
        );

    }
}


/* --------------------------------
   SOURCE MODAL
-------------------------------- */

function openSourceModal(streamId) {

    const stream =
        streams.find(
            item => item.id === streamId
        );

    if (!stream) {
        return;
    }

    currentModalStream =
        streamId;

    document.getElementById(
        "modalStreamName"
    ).textContent =
        stream.name;

    document.getElementById(
        "modalSource"
    ).value =
        stream.source || "";

    document
        .getElementById("sourceModal")
        .classList.remove("hidden");

}


function closeSourceModal() {

    currentModalStream = null;

    document
        .getElementById("sourceModal")
        .classList.add("hidden");

}


document
    .getElementById("closeModal")
    .addEventListener(
        "click",
        closeSourceModal
    );


document
    .getElementById("cancelModal")
    .addEventListener(
        "click",
        closeSourceModal
    );


document
    .getElementById("sourceForm")
    .addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            if (!currentModalStream) {
                return;
            }

            const source =
                document
                    .getElementById("modalSource")
                    .value
                    .trim();

            if (!source) {

                showToast(
                    "Source URL is required"
                );

                return;
            }


            try {

                await api(
                    `/api/streams/${currentModalStream}/source`,
                    {
                        method: "PUT",

                        body: JSON.stringify({
                            source
                        })
                    }
                );


                await api(
                    `/api/streams/${currentModalStream}/start`,
                    {
                        method: "POST"
                    }
                );


                closeSourceModal();

                showToast(
                    "Source added and stream started"
                );

                await loadStreams();

            } catch (error) {

                showToast(
                    error.message
                );

            }

        }
    );


/* --------------------------------
   STREAM RENDERING
-------------------------------- */

function renderDashboardStreams() {

    const container =
        document.getElementById(
            "dashboardStreams"
        );

    if (!streams.length) {

        container.innerHTML = `
            <div class="empty-state">
                No streams created yet.
            </div>
        `;

        return;
    }


    const items =
        streams.slice(0, 6);


    container.innerHTML =
        items.map(stream => {

            let statusHtml = "";

            if (stream.running) {

                statusHtml = `
                    <span class="live-status">
                        <span class="status-dot"></span>
                        LIVE
                    </span>
                `;

            } else if (stream.source) {

                statusHtml = `
                    <span class="ready-status">
                        READY
                    </span>
                `;

            } else {

                statusHtml = `
                    <span class="scheduled-status">
                        SCHEDULED
                    </span>
                `;

            }


            return `
                <div class="stream-row">

                    <div>
                        <div class="stream-name">
                            ${escapeHtml(stream.name)}
                        </div>

                        <div class="stream-id">
                            ID: ${escapeHtml(stream.id)}
                        </div>
                    </div>

                    <div>
                        ${statusHtml}
                    </div>

                    <div>
                        ${formatNumber(stream.viewers)}
                        viewers
                    </div>

                    <div>
                        ${
                            stream.running
                                ? `
                                    <button
                                        class="btn danger small"
                                        onclick="stopStream('${stream.id}')"
                                    >
                                        Stop
                                    </button>
                                `
                                : stream.source
                                    ? `
                                        <button
                                            class="btn primary small"
                                            onclick="startStream('${stream.id}')"
                                        >
                                            Start
                                        </button>
                                    `
                                    : `
                                        <button
                                            class="btn primary small"
                                            onclick="openSourceModal('${stream.id}')"
                                        >
                                            Add Stream
                                        </button>
                                    `
                        }
                    </div>

                </div>
            `;

        }).join("");

}


function renderLiveStreams() {

    const container =
        document.getElementById(
            "streamsContainer"
        );


    if (!streams.length) {

        container.innerHTML = `
            <div class="empty-state">
                No streams are currently configured.
            </div>
        `;

        return;
    }


    container.innerHTML =
        streams.map(stream => {

            if (!stream.running) {

                return `
                    <div class="live-card scheduled-card">

                        <div class="live-card-top">

                            <div>
                                <div class="live-title">
                                    ${escapeHtml(stream.name)}
                                </div>

                                <div class="live-id">
                                    ID: ${escapeHtml(stream.id)}
                                </div>
                            </div>

                            ${
                                stream.source
                                    ? `
                                        <div class="ready-status">
                                            READY
                                        </div>
                                    `
                                    : `
                                        <div class="scheduled-status">
                                            SCHEDULED
                                        </div>
                                    `
                            }

                        </div>


                        <div class="live-time">
                            ${stream.source
                                ? "READY"
                                : "SCHEDULED"}
                        </div>

                        <div class="live-time-label">
                            ${
                                stream.source
                                    ? "Source available"
                                    : "Waiting for source"
                            }
                        </div>


                        <div class="live-actions">

                            ${
                                stream.source
                                    ? `
                                        <button
                                            class="btn primary"
                                            onclick="startStream('${stream.id}')"
                                        >
                                            ▶ Start
                                        </button>
                                    `
                                    : `
                                        <button
                                            class="btn primary"
                                            onclick="openSourceModal('${stream.id}')"
                                        >
                                            ＋ Add Stream
                                        </button>
                                    `
                            }

                            <button
                                class="btn danger"
                                onclick="deleteStream('${stream.id}')"
                            >
                                Delete
                            </button>

                        </div>

                    </div>
                `;

            }


            return `
                <div
                    class="live-card"
                    data-stream-id="${stream.id}"
                >

                    <div class="live-card-top">

                        <div>

                            <div class="live-title">
                                ${escapeHtml(stream.name)}
                            </div>

                            <div class="live-id">
                                ID: ${escapeHtml(stream.id)}
                            </div>

                        </div>

                        <div class="live-badge">

                            <span class="status-dot"></span>

                            LIVE

                        </div>

                    </div>


                    <div
                        class="live-time"
                        data-timer="${stream.id}"
                    >
                        ${formatDuration(
                            stream.started_at
                        )}
                    </div>

                    <div class="live-time-label">
                        STREAM DURATION
                    </div>


                    <div class="live-meta">

                        <div class="meta-box">

                            <span>
                                Viewers
                            </span>

                            <strong>
                                ${formatNumber(
                                    stream.viewers
                                )}
                            </strong>

                        </div>


                        <div class="meta-box">

                            <span>
                                Stream ID
                            </span>

                            <strong>
                                ${escapeHtml(
                                    stream.id
                                )}
                            </strong>

                        </div>

                    </div>


                    <div class="live-actions">

                        <button
                            class="btn"
                            onclick="copyM3u8('${stream.id}')"
                        >
                            Copy M3U8
                        </button>

                        <button
                            class="btn danger"
                            onclick="stopStream('${stream.id}')"
                        >
                            Stop
                        </button>

                    </div>

                </div>
            `;

        }).join("");

}


/* --------------------------------
   DELETE
-------------------------------- */

async function deleteStream(streamId) {

    const stream =
        streams.find(
            item => item.id === streamId
        );

    const confirmed =
        window.confirm(
            `Delete "${stream?.name || "this stream"}"?`
        );

    if (!confirmed) {
        return;
    }


    try {

        await api(
            `/api/streams/${streamId}`,
            {
                method: "DELETE"
            }
        );

        showToast(
            "Stream deleted"
        );

        await loadStreams();

    } catch (error) {

        showToast(
            error.message
        );

    }

}


/* --------------------------------
   HEALTH
-------------------------------- */

async function loadHealth() {

    try {

        const data =
            await api(
                "/api/health/stats"
            );


        const cpu =
            Number(
                data.cpu?.percent || 0
            );

        const ram =
            Number(
                data.memory?.percent || 0
            );


        document.getElementById(
            "dashboardActive"
        ).textContent =
            formatNumber(
                data.active_streams
            );


        document.getElementById(
            "dashboardViewers"
        ).textContent =
            formatNumber(
                data.total_viewers
            );


        document.getElementById(
            "dashboardCpu"
        ).textContent =
            `${cpu.toFixed(1)}%`;


        document.getElementById(
            "dashboardRam"
        ).textContent =
            `${ram.toFixed(1)}%`;


        document.getElementById(
            "healthActive"
        ).textContent =
            formatNumber(
                data.active_streams
            );


        document.getElementById(
            "healthViewers"
        ).textContent =
            formatNumber(
                data.total_viewers
            );


        document.getElementById(
            "healthViewers2"
        ).textContent =
            formatNumber(
                data.total_viewers
            );


        document.getElementById(
            "healthStreams"
        ).textContent =
            formatNumber(
                data.total_streams
            );


        document.getElementById(
            "healthCpu"
        ).textContent =
            `${cpu.toFixed(1)}%`;


        document.getElementById(
            "healthRam"
        ).textContent =
            `${ram.toFixed(1)}%`;


        document.getElementById(
            "cpuBar"
        ).style.width =
            `${Math.min(cpu, 100)}%`;


        document.getElementById(
            "ramBar"
        ).style.width =
            `${Math.min(ram, 100)}%`;


        document.getElementById(
            "healthUptime"
        ).textContent =
            formatUptime(
                data.uptime_seconds
            );


        document.getElementById(
            "sidebarUptime"
        ).textContent =
            `Uptime ${formatUptime(
                data.uptime_seconds
            )}`;


    } catch (error) {

        console.error(
            "Health error:",
            error
        );

    }

}


/* --------------------------------
   STREAMS LOAD
-------------------------------- */

async function loadStreams() {

    try {

        const data =
            await api(
                "/api/streams"
            );

        streams =
            data.streams || [];


        renderDashboardStreams();

        renderLiveStreams();


    } catch (error) {

        console.error(
            "Streams error:",
            error
        );

    }

}


/* --------------------------------
   LIVE TIMERS
-------------------------------- */

function updateTimers() {

    document
        .querySelectorAll(
            "[data-timer]"
        )
        .forEach(element => {

            const streamId =
                element.dataset.timer;

            const stream =
                streams.find(
                    item =>
                        item.id === streamId
                );

            if (!stream) {
                return;
            }

            element.textContent =
                formatDuration(
                    stream.started_at
                );

        });

}


/* --------------------------------
   REFRESH
-------------------------------- */

async function refresh() {

    await Promise.all([
        loadStreams(),
        loadHealth()
    ]);

}


refresh();


setInterval(
    refresh,
    3000
);


setInterval(
    updateTimers,
    1000
);
