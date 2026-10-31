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

## Entity Viewer pin

`Plugins/EntityViewer.xml` pins Entity Viewer 0.1.12 at commit
`95143142acdebc9287aabab6c9a0f0dd8164c70c`, including
[viewer #15](https://github.com/CometWorks/viewer/pull/15). Viewer iframe URLs,
dialog module imports and asset-setup API requests preserve Quasar's hosted panel
path prefix while continuing to support root hosting. Hosted enrollment requires
the matching Quasar build from
[Quasar #318](https://github.com/CometWorks/quasar/pull/318).

The replay improvements from [viewer #12](https://github.com/CometWorks/viewer/pull/12)
remain included. Incidents close after one minute without meaningful
activity, continue up to a configurable duration (15 minutes by default, one hour
maximum), and expand through connected activity from 500 m to a configurable
10 km radius. The history view exposes these settings and recorded incident
boundaries, and applies context changes correctly when seeking backward.

The companion reuses suppressed sample buffers, avoids replay-object allocations
for unchanged block audits, caches layout dependencies, and reduces repeated worker
and archive-index scans. Emitted evidence keeps independent ownership. Reproducible
benchmarks and regression checks cover these optimizations in viewer #12.

Capture, terrain and query budgets remain bounded; very dense recordings can
require shorter loaded ranges. Existing recordings remain readable. Recording
stays opt-in and administrator-only, with a 1 Hz baseline, 5 Hz incident target,
24-hour retention, historical geometry and window-lifetime asset caching.

This pin requires **Quasar 1.3.0.4 or newer**, the first release containing the
background companion discovery API from
[Quasar #198](https://github.com/CometWorks/quasar/pull/198). Update Quasar before
updating Entity Viewer and its Magnetar companion.

Quasar installs plugin source from the exact catalog commit, so this update does
not require a separate viewer binary release. Once the catalog change is merged,
update Entity Viewer from Quasar's UI plugin catalog, update its companion on the
managed servers, and restart Quasar to load the updated plugin. Capture budgets,
storage quotas, model availability and omitted rendering details are documented
in the pinned source's [replay guide](https://github.com/CometWorks/viewer/blob/95143142acdebc9287aabab6c9a0f0dd8164c70c/Docs/Replay.md).

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
