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

`Plugins/EntityViewer.xml` pins the viewer fixes in
[viewer #4](https://github.com/CometWorks/viewer/pull/4), commit
`472af9579f5028f5d21d3e8b3fea546073f8a15b`. Recording history is integrated into the main Entity Viewer
panel, and entity-list alignment and the history navigation icon are corrected.
The pin includes the existing administrator-only replay system with a 1 Hz
baseline, 5 Hz incident capture, up to 24 hours of retention, and recorded grid
layouts/destruction for grids up to 50,000 blocks.

This pin requires **Quasar 1.3.0.4 or newer**, the first release containing the
background companion discovery API from
[Quasar #198](https://github.com/CometWorks/quasar/pull/198). Update Quasar before
updating Entity Viewer and its Magnetar companion.

Quasar installs plugin source from the exact catalog commit, so this update does
not require a separate viewer binary release. Once the catalog change is merged,
update Entity Viewer from Quasar's UI plugin catalog, update its companion on the
managed servers, and restart Quasar to load the updated plugin. Capture budgets,
storage quotas, model availability and omitted rendering details are documented
in the pinned source's [replay guide](https://github.com/CometWorks/viewer/blob/472af9579f5028f5d21d3e8b3fea546073f8a15b/Docs/Replay.md).

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
