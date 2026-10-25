<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img src="assets/banner-light.svg" alt="Abdelmonem Awad — self-hosted tools for machines that run unattended" width="100%">
</picture>

Hi, I'm Abdelmonem. I build self-hosted software for hardware that is supposed to look after itself — and, lately, drivers for hardware that refuses to be driven at all. Most of it is Python, TypeScript and C, and almost all of it ships in Arabic as well as English, because the people running this hardware do not all read English.

## os-xgs-npu — reclaiming a family of firewalls

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/thanks-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/thanks-light.svg">
  <img src="assets/thanks-light.svg" alt="With thanks to the OPNsense project and Deciso, for OPNsense itself, the open firewall this whole project is built on, and for the openness and advice they have given it along the way. os-xgs-npu is an independent project, not affiliated with or endorsed by OPNsense, Deciso or Sophos." width="100%">
</picture>

Install OPNsense on a Sophos XGS and it boots with **no network interfaces at all**: every front port belongs to a coprocessor behind PCIe, with drivers for Linux and the vendor's own OS only. **[os-xgs-npu](https://github.com/AbdelmonemAwad/os-xgs-npu)** is the FreeBSD drivers and the OPNsense plugin that hand those ports back, then give the coprocessor the firewall's own connections and IPsec, so they no longer cross the host. Two of the six coprocessor families answer now.

**[npuforge.org](https://npuforge.org)** · [the guide](https://npuforge.org/docs/guide/step-by-step/) · [ready-made images](https://build.npuforge.org) · [releases](https://github.com/AbdelmonemAwad/os-xgs-npu/releases) · [the story](https://npuforge.org/story/) · [in Arabic](https://npuforge.org/ar/)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://npuforge.org/readme/status-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://npuforge.org/readme/status-light.svg">
  <img src="https://npuforge.org/readme/status-light.svg" alt="os-xgs-npu status, drawn by the project itself: the stage it is at, the same features on both appliances side by side — run, partial or not built yet — what has been measured on each, and how far along each one is" width="100%">
</picture>

<div align="center">

| Measured | |
|:---:|:---|
| **[9,837 Mbit/s](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/measurements/xgs3300-many-2026-10-19.md)** | a thousand connections through an XGS 3300, its processors 7.8 % busy |
| **[941 Mbit/s](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/measurements/xgs136-hardware-2026-10-18.md)** | through an XGS 136 in hardware at 0.4 %, against 19.6 % through the host |
| **[9,019 Mbit/s](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/measurements/many-tunnels-3300-2026-10-20.md)** | sixteen IPsec tunnels at once between two XGS 3300s |
| **[10 frames, not 610,533](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/measurements/verdict-2026-10-23.md)** | what a UDP flood cut in hardware still sent the host |
| **[29 discoveries](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/findings/discoveries-2026-10-22.md)** | in the vendor's own sources, every one measured within three days |

</div>

- **Fast, and still a firewall.** Block lists, JA4 fingerprints, IPsec policies, the Traffic Shaper and the Captive Portal still decide over a connection in hardware, and with Inspect, then hardware, Suricata sees each connection's start before the coprocessor carries the rest.
- **Two roads onto an appliance.** A ready-made image with every release, or one built to order in the browser, and a guide from nothing to the first sign-in. Updates come from its own page in OPNsense.
- **Owners run it too.** It is an alpha: the XGS 136 and the XGS 3300 run here, an XGS 126 runs for two owners, and every other model installs and checks its own ports, untested until someone reports back. [Tell me how yours goes.](https://github.com/AbdelmonemAwad/os-xgs-npu/issues/new?template=appliance.yml)
- **It keeps its own score.** Every figure has a page saying how it was measured, and the completion figures went down when the discoveries were found. Both appliances stand at 96 %.

> The repository went public on 25 September 2026; the work behind it took close to two years.
> **[The whole story is on the site.](https://npuforge.org/story/)**

<details>
<summary>How each family is driven</summary>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/octeon-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/octeon-light.svg">
  <img src="assets/octeon-light.svg" alt="The Cavium path: OPNsense host, eight virtual functions, handshake and facilities, eight SDP rings, the CN83XX fast path, twelve front ports" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/npu-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/npu-light.svg">
  <img src="assets/npu-light.svg" alt="The Marvell path: OPNsense host, npuep module, PCIe BAR, one queue pair, the CN9131 coprocessor, fourteen front ports" width="100%">
</picture>

</details>

## OPNsense plugins

Ten plugins, BSD-2 licensed and packaged as FreeBSD ports. Each works on its own. With os-xgs-npu installed, their pages join the XGS section of the menu, and the project's own update keeps them current and adds the ones that suit the appliance.

<div align="center">

| Plugin | What it does |
|:---:|:---|
| **[os-linkhealth](https://github.com/AbdelmonemAwad/os-linkhealth)** | names the cable or transceiver that is going bad, before the link drops |
| **[os-netreport](https://github.com/AbdelmonemAwad/os-netreport)** | scheduled network reports and new-device alerts by email, in the GUI's language |
| **[os-frontpanel](https://github.com/AbdelmonemAwad/os-frontpanel)** | the appliance's LCD and buttons, through LCDproc |
| **[os-fanctl](https://github.com/AbdelmonemAwad/os-fanctl)** | fan control and every readable temperature sensor |
| **[os-theme-xgs](https://github.com/AbdelmonemAwad/os-theme-xgs)** | XGS Silicon: a light, a dark and an automatic theme, Arabic included |
| **[os-kernelfollow](https://github.com/AbdelmonemAwad/os-kernelfollow)** | rebuilds an out-of-tree driver for the new kernel before an update's reboot |
| **[os-watchdog](https://github.com/AbdelmonemAwad/os-watchdog)** | arms the host's hardware watchdog, and reads why it last reset |
| **[os-fallbackcrypto](https://github.com/AbdelmonemAwad/os-fallbackcrypto)** | chooses the kernel's crypto driver for the tunnels the host carries itself |
| **[os-blocklists](https://github.com/AbdelmonemAwad/os-blocklists)** | address, DNS, country and JA4 block lists on one page |
| **[os-portguard](https://github.com/AbdelmonemAwad/os-portguard)** | Layer 2 rules: a device blocked by its MAC address |

</div>

Planned: [traffic priority](https://github.com/AbdelmonemAwad/os-trafficpriority).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/stack-light.svg">
  <img src="assets/stack-light.svg" alt="Plugin layers: web GUI, MVC API, configd, Python backend, FreeBSD" width="100%">
</picture>

They follow OPNsense's own shape, so they are backed up, upgraded and translated like every other part of the system.

## Arabic and right-to-left

- **[opnsense-arabic](https://github.com/AbdelmonemAwad/opnsense-arabic)** — the Arabic translation of the OPNsense 26.7 web interface, the XGS plugins' strings included.
- **[opnsense-rtl](https://github.com/AbdelmonemAwad/opnsense-rtl)** — right-to-left layout for Arabic and Persian.

npuforge.org has [an Arabic edition](https://npuforge.org/ar/) of its own, and every page the XGS work adds to OPNsense is [photographed in both languages](https://npuforge.org/docs/guide/the-pages/).

## FilaMind — Klipper and Moonraker

[FilaMind](https://github.com/filamind-app) is an open-source, self-hosted suite for makers running Klipper and Moonraker.

- **[filamind-core](https://github.com/filamind-app/filamind-core)** — the TypeScript foundation: a Moonraker client, a fail-closed write arbiter, 19 locales.
- **[filamind-flow](https://github.com/filamind-app/filamind-flow)** — the control panel: firmware flashing, input shaping, TMC tooling.
- **[filamind-screen](https://github.com/filamind-app/filamind-screen)** — the on-printer touch interface, with Tauri 2.
- **[filamind-3d](https://github.com/filamind-app/filamind-3d)** — the web control UI.
- **[filamind-ai](https://github.com/filamind-app/filamind-ai)** — private AI on a Synology NAS, in Arabic and English.
- **[filamind-setup](https://github.com/filamind-app/filamind-setup)** — one installer, as a CLI and as a widget.

## Odoo

Most of my Odoo work is client projects in private repositories. The public part is the device side:

- **[filamind-iot](https://github.com/deltafabs/filamind-iot)** — a self-hosted IoT gateway addon for Odoo 19.
- **[filamind-iotbox](https://github.com/deltafabs/filamind-iotbox)** — an Odoo IoT Box image that takes a server URL directly.
- **[filamind-iot-proxy](https://github.com/deltafabs/filamind-iot-proxy)** — pairing, certificates and a reverse tunnel, on your own machine.

## cadenza

**[cadenza](https://github.com/AbdelmonemAwad/cadenza)** curates music libraries on a Synology NAS: acoustic fingerprinting for real duplicates, metadata from several sources, format conversion. It never deletes anything; suspect files go to quarantine.

## What I use

Python, C for the kernel side, TypeScript and Vue 3, PHP and Volt for OPNsense, Rust where Tauri needs it. Underneath: FreeBSD and its ports tree, Synology DSM 7, Docker, FastAPI and GitHub Actions. iOS and Android apps and the Odoo client work stay in private repositories.

Questions about the XGS drivers are best asked in [the project's Discussions](https://github.com/AbdelmonemAwad/os-xgs-npu/discussions), where the answer stays for the next person. If the XGS work is useful to you, **[sponsoring it](https://github.com/sponsors/AbdelmonemAwad)** pays for the appliances, modules and test gear the next families need.

## Recently merged

<!-- merged starts -->
- [GUI: the coprocessor's console, fast-path counters, watchdog and memory errors, PCIe ordering, IPsec counts](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/785) — **os-xgs-npu**, 25 Oct
- [os-xgs-npu: the coprocessor console page, fast-path counters, watchdog and memory errors, in Arabic](https://github.com/AbdelmonemAwad/opnsense-arabic/pull/34) — **opnsense-arabic**, 25 Oct
- [XGS: Overview's Coprocessor tab: summary cards, and the vendor's build by that name](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/784) — **os-xgs-npu**, 25 Oct
- [os-xgs-npu: the Coprocessor tab's summary cards and the vendor's build, in Arabic](https://github.com/AbdelmonemAwad/opnsense-arabic/pull/33) — **opnsense-arabic**, 25 Oct
- [XGS: Overview: a Coprocessor tab - its software, chips, flash and eMMC, read-only](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/783) — **os-xgs-npu**, 25 Oct
- [os-xgs-npu: XGS: Overview's Coprocessor tab, in Arabic](https://github.com/AbdelmonemAwad/opnsense-arabic/pull/32) — **opnsense-arabic**, 25 Oct
<!-- merged ends -->
