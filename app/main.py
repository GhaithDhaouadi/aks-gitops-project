from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import socket
import datetime

app = FastAPI(title="AKS GitOps Demo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ENV_CONFIGS = {
    "dev": {
        "accent": "#4fc3f7",
        "accent_dim": "#1a3a4a",
        "label": "DEVELOPMENT",
        "status": "DEV BUILD",
    },
    "staging": {
        "accent": "#ffb74d",
        "accent_dim": "#3a2a0a",
        "label": "STAGING",
        "status": "PRE-RELEASE",
    },
    "prod": {
        "accent": "#69f0ae",
        "accent_dim": "#0a3a20",
        "label": "PRODUCTION",
        "status": "LIVE",
    },
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GitOps / {env_label}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --accent:     {accent};
      --accent-dim: {accent_dim};
      --bg:         #080c10;
      --surface:    #0d1117;
      --border:     #1c2330;
      --text:       #c9d1d9;
      --muted:      #484f58;
      --mono:       'IBM Plex Mono', monospace;
      --sans:       'IBM Plex Sans', sans-serif;
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: var(--sans);
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: 0;
      overflow-x: hidden;
    }}

    /* ── Top bar ── */
    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 32px;
      height: 48px;
      border-bottom: 1px solid var(--border);
      background: var(--surface);
      position: sticky;
      top: 0;
      z-index: 10;
    }}

    .topbar-left {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}

    .logo-mark {{
      width: 20px;
      height: 20px;
      border: 2px solid var(--accent);
      transform: rotate(45deg);
      flex-shrink: 0;
    }}

    .topbar-title {{
      font-family: var(--mono);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: var(--text);
      text-transform: uppercase;
    }}

    .env-badge {{
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.12em;
      padding: 3px 10px;
      background: var(--accent-dim);
      color: var(--accent);
      border: 1px solid var(--accent);
      border-radius: 2px;
      text-transform: uppercase;
    }}

    .topbar-right {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
    }}

    .pulse {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #69f0ae;
      animation: blink 2.4s ease-in-out infinite;
    }}

    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50%       {{ opacity: 0.25; }}
    }}

    /* ── Main layout ── */
    .main {{
      flex: 1;
      display: grid;
      grid-template-columns: 220px 1fr;
      min-height: calc(100vh - 48px);
    }}

    /* ── Sidebar ── */
    .sidebar {{
      border-right: 1px solid var(--border);
      padding: 28px 0;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .sidebar-section {{
      padding: 0 16px 12px;
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: 0.14em;
      color: var(--muted);
      text-transform: uppercase;
      margin-top: 20px;
    }}

    .sidebar-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 7px 20px;
      font-size: 13px;
      color: var(--muted);
      cursor: default;
      transition: color 0.15s, background 0.15s;
      border-left: 2px solid transparent;
    }}

    .sidebar-item.active {{
      color: var(--accent);
      border-left-color: var(--accent);
      background: var(--accent-dim);
      font-weight: 500;
    }}

    .sidebar-item .dot {{
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: currentColor;
      opacity: 0.5;
      flex-shrink: 0;
    }}

    .sidebar-item.active .dot {{ opacity: 1; }}

    /* ── Content ── */
    .content {{
      padding: 36px 40px;
      display: flex;
      flex-direction: column;
      gap: 32px;
      overflow-y: auto;
    }}

    .section-title {{
      font-family: var(--mono);
      font-size: 11px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-title::after {{
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }}

    /* ── Stat cards ── */
    .stat-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1px;
      background: var(--border);
      border: 1px solid var(--border);
      border-radius: 4px;
      overflow: hidden;
    }}

    .stat-card {{
      background: var(--surface);
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: background 0.15s;
    }}

    .stat-card:hover {{ background: #111620; }}

    .stat-label {{
      font-family: var(--mono);
      font-size: 10px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .stat-value {{
      font-family: var(--mono);
      font-size: 16px;
      font-weight: 500;
      color: var(--accent);
      word-break: break-all;
      line-height: 1.3;
    }}

    /* ── Stack list ── */
    .stack-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .stack-tag {{
      font-family: var(--mono);
      font-size: 12px;
      padding: 5px 14px;
      border: 1px solid var(--border);
      border-radius: 2px;
      color: var(--text);
      background: var(--surface);
      letter-spacing: 0.04em;
    }}

    /* ── Log panel ── */
    .log-panel {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 16px 20px;
      font-family: var(--mono);
      font-size: 12px;
      line-height: 1.9;
    }}

    .log-line {{
      display: flex;
      gap: 16px;
    }}

    .log-ts   {{ color: var(--muted); flex-shrink: 0; }}
    .log-tag  {{ color: var(--accent); flex-shrink: 0; width: 52px; }}
    .log-msg  {{ color: var(--text); }}

    /* ── Endpoint list ── */
    .endpoint-list {{
      display: flex;
      flex-direction: column;
      gap: 1px;
      border: 1px solid var(--border);
      border-radius: 4px;
      overflow: hidden;
    }}

    .endpoint-row {{
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 12px 20px;
      background: var(--surface);
      font-family: var(--mono);
      font-size: 13px;
      transition: background 0.15s;
    }}

    .endpoint-row:hover {{ background: #111620; }}

    .method {{
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 0.1em;
      padding: 2px 8px;
      border-radius: 2px;
      background: var(--accent-dim);
      color: var(--accent);
      border: 1px solid var(--accent);
      flex-shrink: 0;
    }}

    .ep-path  {{ color: var(--text); flex: 1; }}
    .ep-desc  {{ color: var(--muted); font-size: 11px; }}

    /* ── Footer ── */
    .footer {{
      padding: 14px 32px;
      border-top: 1px solid var(--border);
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
      display: flex;
      justify-content: space-between;
      background: var(--surface);
    }}

    @media (max-width: 640px) {{
      .main  {{ grid-template-columns: 1fr; }}
      .sidebar {{ display: none; }}
      .content {{ padding: 24px 20px; }}
    }}
  </style>
</head>
<body>

<!-- Top bar -->
<header class="topbar">
  <div class="topbar-left">
    <div class="logo-mark"></div>
    <span class="topbar-title">AKS / GitOps</span>
    <span class="env-badge">{env_label}</span>
  </div>
  <div class="topbar-right">
    <div class="pulse"></div>
    SYNC ACTIVE &nbsp;|&nbsp; {status}
  </div>
</header>

<div class="main">

  <!-- Sidebar -->
  <nav class="sidebar">
    <div class="sidebar-section">Navigation</div>
    <div class="sidebar-item active"><span class="dot"></span> Overview</div>
    <div class="sidebar-item"><span class="dot"></span> Metrics</div>
    <div class="sidebar-item"><span class="dot"></span> Deployments</div>
    <div class="sidebar-item"><span class="dot"></span> Logs</div>

    <div class="sidebar-section">Links</div>
    <div class="sidebar-item"><span class="dot"></span> Health Check</div>
    <div class="sidebar-item"><span class="dot"></span> API Docs</div>
    <div class="sidebar-item"><span class="dot"></span> System Info</div>
  </nav>

  <!-- Main content -->
  <section class="content">

    <!-- Runtime stats -->
    <div>
      <div class="section-title">Runtime</div>
      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-label">Environment</div>
          <div class="stat-value">{env_upper}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Version</div>
          <div class="stat-value">{version}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Pod Hostname</div>
          <div class="stat-value">{hostname}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Server Time</div>
          <div class="stat-value">{current_time}</div>
        </div>
      </div>
    </div>

    <!-- Tech stack -->
    <div>
      <div class="section-title">Stack</div>
      <div class="stack-grid">
        <span class="stack-tag">Azure Kubernetes Service</span>
        <span class="stack-tag">Flux v2</span>
        <span class="stack-tag">Azure DevOps</span>
        <span class="stack-tag">Terraform</span>
        <span class="stack-tag">FastAPI</span>
        <span class="stack-tag">Docker</span>
      </div>
    </div>

    <!-- Endpoints -->
    <div>
      <div class="section-title">Endpoints</div>
      <div class="endpoint-list">
        <div class="endpoint-row">
          <span class="method">GET</span>
          <span class="ep-path">/</span>
          <span class="ep-desc">Dashboard UI</span>
        </div>
        <div class="endpoint-row">
          <span class="method">GET</span>
          <span class="ep-path">/health</span>
          <span class="ep-desc">Liveness probe</span>
        </div>
        <div class="endpoint-row">
          <span class="method">GET</span>
          <span class="ep-path">/info</span>
          <span class="ep-desc">Service metadata</span>
        </div>
        <div class="endpoint-row">
          <span class="method">GET</span>
          <span class="ep-path">/docs</span>
          <span class="ep-desc">OpenAPI spec</span>
        </div>
      </div>
    </div>

    <!-- Activity log -->
    <div>
      <div class="section-title">Activity</div>
      <div class="log-panel">
        <div class="log-line">
          <span class="log-ts">{current_time}</span>
          <span class="log-tag">INFO</span>
          <span class="log-msg">Application started — environment={env_upper}</span>
        </div>
        <div class="log-line">
          <span class="log-ts">{current_time}</span>
          <span class="log-tag">INFO</span>
          <span class="log-msg">Flux v2 sync interval: 1m — source reconciled</span>
        </div>
        <div class="log-line">
          <span class="log-ts">{current_time}</span>
          <span class="log-tag">OK</span>
          <span class="log-msg">Health probe passing on pod/{hostname}</span>
        </div>
      </div>
    </div>

  </section>
</div>

<footer class="footer">
  <span>Ghaith Dhaouadi &mdash; Cloud DevOps Engineer</span>
  <span>AKS GitOps Demo &nbsp;/&nbsp; {version}</span>
</footer>

</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def read_root():
    env     = os.getenv("ENVIRONMENT", "dev")
    version = os.getenv("APP_VERSION", "v1.0.0")
    cfg     = ENV_CONFIGS.get(env, ENV_CONFIGS["dev"])

    return HTML_TEMPLATE.format(
        env_label    = cfg["label"],
        env_upper    = env.upper(),
        accent       = cfg["accent"],
        accent_dim   = cfg["accent_dim"],
        status       = cfg["status"],
        version      = version,
        hostname     = socket.gethostname()[:22],
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.get("/health")
def health():
    return {
        "status":      "healthy",
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "version":     os.getenv("APP_VERSION", "v1.0.0"),
        "hostname":    socket.gethostname(),
        "timestamp":   datetime.datetime.now().isoformat(),
    }


@app.get("/info")
def info():
    return {
        "service":     "AKS GitOps Demo",
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "version":     os.getenv("APP_VERSION", "v1.0.0"),
        "kubernetes": {
            "pod_name":  socket.gethostname(),
            "namespace": os.getenv("KUBERNETES_NAMESPACE", "unknown"),
            "pod_ip":    os.getenv("KUBERNETES_POD_IP", "unknown"),
        },
        "gitops": {
            "tool":          "Flux v2",
            "sync_interval": "1m",
        },
    }
