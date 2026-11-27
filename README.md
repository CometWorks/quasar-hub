# QuasarHub

This repository is the public manifest catalog for
[Quasar](https://github.com/CometWorks/quasar) UI plugins.

QuasarHub works like MagnetarHub: it does not host plugin source. It holds small
XML descriptors that point to reviewed plugin repositories and pinned commits.
Quasar can then discover, build, download, and enable UI plugins from those
manifests.

## Repository Roles

- `quasar-hub`
  - reviewed plugin manifests only
  - one XML file per published Quasar UI plugin
  - pinned repository and commit metadata
- `quasar-plugin-template`
  - starter repository for new Quasar UI plugins
  - shows native HTML/Razor UI layout, nav/page contribution, and companion-channel
    conventions
- plugin repositories
  - own plugin source code
  - own plugin package manifest: `quasar-plugin.json`
  - may include shared contracts for companion Magnetar plugins

## Adding a Plugin

1. Start from [Quasar Plugin Template](https://github.com/CometWorks/quasar-plugin-template).
2. Build your plugin in its own GitHub repository.
3. Use native HTML/Razor controls and Quasar appearance tokens so plugin UI
   follows the host's theme and interaction conventions. Scope plugin CSS.
4. Add a `quasar-plugin.json` package manifest to your plugin repository.
5. Add an XML descriptor to `Plugins/` in this repository. Use
   [SamplePlugin.xml](SamplePlugin.xml) as the reference.
6. Pin the descriptor to an exact commit.
7. Submit a pull request for review.

Private development is fine, but published plugins must be in public
repositories before review.

## Descriptor Fields

Required fields:

- `Id`
  Stable plugin id. Generate once and never change it.
- `RepoId`
  GitHub repository id, for example `CometWorks/entity-viewer`.
- `FriendlyName`
  Display name shown in Quasar.
- `Author`
  Plugin author or team.
- `Tooltip`
  Short one-line description.
- `Description`
  Longer details for the plugin panel.
- `PluginKind`
  Use `QuasarUiPlugin`.
- `ProjectPath`
  Relative path to the plugin project file inside the repository.
- `PackageManifest`
  Relative path to the plugin package manifest. Default convention:
  `quasar-plugin.json`.
- `Commit`
  Exact Git commit Quasar should use.

Optional fields:

- `QuasarVersion`
  Version range supported by the plugin.
- `DependencyIds`
  Other Quasar UI plugins this plugin depends on.
- `CompanionPluginIds`
  Magnetar plugins expected on managed Dedicated Servers.
- `Platforms`
  `Windows`, `Linux`, or both.
- `Hidden`
  Hide dependency-only plugins from normal selection.
- `Recommended`
  Highlight the plugin in Quasar's UI plugin catalog without installing it.
  Recommended plugins remain opt-in.
- `ImplicitLoading`
  Install or update this reviewed plugin automatically from QuasarHub. First
  install enables it for the next Quasar restart; later implicit updates keep a
  user-disabled plugin disabled.
- `AlternateVersions`
  Named alternate commits for test or custom builds.

## King of the Hill

`Plugins/KingOfTheHill.xml` pins King of the Hill from the public,
AGPL-3.0-only [OwendB1/quasar-koth](https://github.com/OwendB1/quasar-koth)
repository. Its `Commit` and `QuasarVersion` are the pinned revision and the
minimum Quasar version; update only the descriptor when the pin moves.

Requires Workshop mod **2388326362** in the world.
Refresh Quasar's UI Plugins catalog, install **King of the Hill**, then restart
Quasar and the managed game servers to load the UI and bundled companion.
Configure a dedicated KOTH channel on the plugin page; announcements and commands
use Quasar's existing bot. Installation remains opt-in (`ImplicitLoading=false`).

The KOTH page follows Quasar's normal content width and heading styles. Servers
use independent expansion panels instead of a dropdown and Refresh button.
Expanded panels and connected-server discovery update every five seconds.
Each panel keeps its own score and reset state, so a slow server does not block
other panels and world changes invalidate only the affected confirmation.

The companion reads live scores and protects the supported mod's plugin-message
handler from client-sent reset packets. Standalone resets verify an XML backup
before clearing scores. Nexus and Quasar cluster resets are refused; node score
views do not sum replicated scores.

The companion answers score polls from a copy it refreshes about once a second
on its own game tick, so polls never wait for the game thread.
During a world save or a physics stall the panel says "Scores are N s old; the
server's game thread is busy." instead of timing out, and a stalled server no
longer delays announcements from the others. Live game and Discord checks are described in the plugin's
[acceptance guide](https://github.com/OwendB1/quasar-koth/blob/main/docs/LiveAcceptance.md).

## Entity Viewer

`Plugins/EntityViewer.xml` pins Entity Viewer from the public
[CometWorks/viewer](https://github.com/CometWorks/viewer) repository. Its
`Commit` and `QuasarVersion` are the pinned revision and the minimum Quasar
version; update only the descriptor when the pin moves. Viewer is opt-in.

Update the viewer adapter, browser assets and Magnetar companion together: the
scene/history SDK envelope carries `{ data, assetSession }`, and asset sessions
are issued only from authorized companion scenes or retained history, never from
browser-selected mod lists. Asset/path limits, response budgets and private
diagnostics apply. Scene, asset and history operations use the authenticated
Quasar browser SDK; the entity columns are a browser assembly loaded by the
Quasar WASM dashboard. Nebula-hosted panels can start over HTTPS and move new
work to WebRTC once a direct connection is confirmed; the hosted tunnel has a
shared 20 Mbit/s limit. Viewer iframe URLs and asset-setup requests keep
Quasar's hosted panel path prefix and also work at the root. The viewer and its
asset setup dialog open through Quasar's native dialog host
(`IQuasarDialogService`), so Entity Viewer 0.1.15 requires Quasar 1.7.1 with
that host (v1.7.1.7 or later).

In the Entities list, Firefox reuses the selected Content and Mods folders when
opening another grid; reloading the page needs the folders selected again.
Unavailable entities show a disabled, crossed-out eye with an explanatory
tooltip.

Remote model, LOD, texture and font loads share a queue with at most two active
asset operations per frame. HTTP 429 responses during asset resolution or
download opening retry with bounded backoff for about one minute; exhausted
throttling stays an error instead of being cached as a missing asset, and
interrupted downloads are not replayed. Local folder loads keep their own
parallelism.

Recording is opt-in and administrator-only, with a 1 Hz baseline, a 5 Hz incident
target, 24-hour retention, historical geometry and window-lifetime asset caching.
Cluster-aware recording/history and offline archives are supported, and existing
recordings stay readable. Incidents close after one minute without meaningful
activity, last up to a configurable duration (15 minutes by default, one hour
maximum), and grow through connected activity from 500 m up to a configurable
10 km radius. The history view shows these settings and recorded incident
boundaries, and seeking backward applies context changes correctly. Capture,
terrain and query budgets are bounded, so very dense recordings can need shorter
loaded ranges.

Quasar installs plugin source from the exact catalog commit, so a pin change
needs no separate viewer binary release. After the catalog change is merged,
update Entity Viewer from Quasar's UI plugin catalog, update its companion on the
managed servers, and restart Quasar. Capture budgets, storage quotas, model
availability and omitted rendering details are in the viewer's
[replay guide](https://github.com/CometWorks/viewer/blob/main/Docs/Replay.md).

## Review Expectations

Quasar UI plugins are trusted code running inside the Quasar process. Review
should check:

- plugin source repository is public
- commit is pinned and exists
- plugin follows Quasar appearance tokens and scopes its UI styles
- built-in page/component replacements are declared clearly
- companion Magnetar plugin usage is documented
- static assets are scoped to the plugin
- no unexpected network, filesystem, or credential behavior
