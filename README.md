<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img src="assets/banner-light.svg" alt="Abdelmonem Awad — self-hosted tools for machines that run unattended" width="100%">
</picture>

Hi, I'm Abdelmonem. I build self-hosted software for hardware that is supposed to look after itself — and, lately, drivers for hardware that refuses to be driven at all. Alongside that: a control suite for Klipper 3D printers, plugins for OPNsense firewalls, local LLM serving on Synology hardware, Odoo modules, and iOS and Android apps.

Most of it is Python, TypeScript and C. Almost all of it ships in Arabic as well as English, because the people running this hardware do not all read English.

## os-xgs-npu — reclaiming a family of firewalls

Install OPNsense on a Sophos XGS and it boots to a working firewall with **no network interfaces at all**. The appliance is two computers, and the second — a coprocessor behind PCIe, with drivers for Linux and the vendor's own OS only — owns every front port, so when support lapses the usual verdict is e-waste. **[os-xgs-npu](https://github.com/AbdelmonemAwad/os-xgs-npu)** is the FreeBSD kernel modules that hand those ports back, written against registers no vendor documents, across a family of six coprocessor generations.

> **The repository is much younger than the work in it.** It went public on 25 September 2026; the work
> behind it took close to two years — eight months of surveying other vendors' appliances, adapters that
> failed, a firmware of my own that ran into a board of many chips, and then the turn every driver here
> stands on: the host learning to speak the coprocessor's own language.
> **[The whole story is in the wiki.](https://github.com/AbdelmonemAwad/os-xgs-npu/wiki)**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/AbdelmonemAwad/os-xgs-npu/raw/main/docs/images/readme/status-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/AbdelmonemAwad/os-xgs-npu/raw/main/docs/images/readme/status-light.svg">
  <img src="https://github.com/AbdelmonemAwad/os-xgs-npu/raw/main/docs/images/readme/status-light.svg" alt="os-xgs-npu status, drawn by the project itself: the stage it is at, the same features on both appliances side by side — run, partial or not built yet — what has been measured on each, and how far along each one is" width="100%">
</picture>

- **Two unrelated coprocessors, one contract.** Marvell and Cavium silicon answer the same kernel offload interface, behind the same OPNsense pages, and both drivers take the same orders: hand one connection back to the host, never offload these addresses or ports.
- **The tunnel costs nothing.** With hardware at both ends, IPsec runs at the rate of clear text — 1.85 Gbit/s on one stream at the standard MTU, 7.41 Gbit/s with jumbo frames.
- **Forwarded at the link's rate.** IPv6 connections handed to the coprocessor carry 9.27 Gbit/s through an XGS 3300 on eight streams, every one of them in hardware — the 10G link is the limit, not the chip. The XGS 136 does the same at its gigabit with the address translation in the coprocessor too: 941 Mbit/s from LAN to WAN with its processors 0.4 % busy, against 19.6 % through the host.
- **What the offload buys is the processor.** Most of a core at a gigabit, against a few hundredths of one, with 99.6 per cent of a connection's frames in hardware.
- **Two roads onto an appliance.** Most people start from a bootable image: **[xgs-image-builder](https://github.com/AbdelmonemAwad/xgs-image-builder)** builds one from [a page in the browser](https://abdelmonemawad.github.io/xgs-image-builder/) with the newest release, the plugins, Arabic and right-to-left already inside, and one built that way has been installed on an XGS 3300 and booted. Experts can load the drivers by hand. Either way it lives in OPNsense as if it belonged there — a menu section of its own, from the overview and the ports to updates and problem reports, in Arabic and English; ports assigned by the names on the chassis at the first boot; and updates from tagged releases since **[0.1.0-alpha.1](https://github.com/AbdelmonemAwad/os-xgs-npu/releases/tag/v0.1.0-alpha.1)**. The next, [0.1.0-alpha.1.1](https://github.com/AbdelmonemAwad/os-xgs-npu/releases/tag/v0.1.0-alpha.1.1), followed the same day, and appliances of both families run it.
- **It keeps its own score.** The main part is done and the rest arrives as updates, but it is an alpha and says so: every figure with its method in [the measurements](https://github.com/AbdelmonemAwad/os-xgs-npu/tree/main/docs/measurements), the dead ends on [the road](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/the-road.md), and plain advice to try a release first on an appliance you can reach.

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

## FilaMind — Klipper and Moonraker

[FilaMind](https://github.com/filamind-app) is an open-source, self-hosted suite for makers running Klipper and Moonraker. Most of my commits over the past year went here.

- **[filamind-core](https://github.com/filamind-app/filamind-core)** — the TypeScript foundation the rest is built on: a Moonraker client, a session orchestrator, a fail-closed write arbiter so two front ends can never fight over the same printer, and i18n for 19 locales.
- **[filamind-flow](https://github.com/filamind-app/filamind-flow)** — the control panel: firmware flashing, input shaping, TMC motor-driver tooling. Python and FastAPI behind Vue 3, built one widget at a time so each piece can be adopted on its own.
- **[filamind-screen](https://github.com/filamind-app/filamind-screen)** — the on-printer touch interface, same core, wrapped as a desktop app with Tauri 2.
- **[filamind-3d](https://github.com/filamind-app/filamind-3d)** — the web control UI on top of the core. Vue 3, Vite and Tailwind over a lean FastAPI host.
- **[filamind-ai](https://github.com/filamind-app/filamind-ai)** — private AI for a Synology NAS: local LLM chat with optional cloud fallback, multi-user, an OpenAI-compatible API, and a full interface in both Arabic and English. Runs on a DVA 3221 with its CUDA GPU, or a DS1821+ on CPU.
- **[filamind-setup](https://github.com/filamind-app/filamind-setup)** — one installer engine behind two front ends, a CLI and a widget inside flow.

## OPNsense plugins

Five plugins, BSD-2 licensed like the platform itself and packaged as FreeBSD ports.

- **[os-linkhealth](https://github.com/AbdelmonemAwad/os-linkhealth)** — watches every physical port and names the cable or transceiver that is going bad, by the label printed on the chassis rather than the interface name. It reads the DOM registers on the transceivers, so the warning arrives before the link actually drops.
- **[os-netreport](https://github.com/AbdelmonemAwad/os-netreport)** — scheduled network reports by email, and an alert the first time an unknown device shows up. Each report is written in whichever language the GUI is set to.
- **[os-frontpanel](https://github.com/AbdelmonemAwad/os-frontpanel)** — drives the LCD and buttons built into an appliance's front panel through LCDproc, with the screens and their timing set from the GUI instead of a config file on disk.
- **[os-fanctl](https://github.com/AbdelmonemAwad/os-fanctl)** — fan control and every readable temperature sensor, for repurposed appliances whose fan curve left with the vendor firmware. Talks to the Super I/O chip directly.
- **[os-theme-xgs](https://github.com/AbdelmonemAwad/os-theme-xgs)** — XGS Silicon, a light, a dark and an automatic theme for the OPNsense GUI on the XGS appliances: carbon and copper like the hardware, IBM Plex with its own Arabic, and not one page's layout changed. An image built for the XGS starts with it.

Three of them now know the Sophos XGS appliances above — port labels for every XGS board and FleXi module, generated from the vendor's own board files, port identification through the coprocessor, temperature and fan readings from the board and from the coprocessor, the 3300's front panel with its buttons and a menu — so a reclaimed box gets more back than its ports. Six packages — the first four here, and the Arabic and right-to-left ones — now follow their latest release by themselves once a day, and survive an OPNsense update that replaces their strings or templates.

They share one shape:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/stack-light.svg">
  <img src="assets/stack-light.svg" alt="Plugin layers: web GUI, MVC API, configd, Python backend, FreeBSD" width="100%">
</picture>

Volt templates and PHP for the interface, the model in XML, configd actions in the middle, and Python doing the real work against FreeBSD. Following that layout instead of inventing my own is what lets the plugins get backed up, upgraded and translated like every other part of the system.

## Odoo

Most of my Odoo work is client projects in private repositories: custom modules and business integrations. The public part is the device side, where Odoo has to talk to real hardware.

- **[filamind-iot](https://github.com/deltafabs/filamind-iot)** — a self-hosted IoT gateway addon for Odoo 19, paired with the IoT-box image below.
- **[filamind-iotbox](https://github.com/deltafabs/filamind-iotbox)** — a patched Odoo IoT Box image that takes a server URL directly on its settings page, instead of going through the hosted pairing service.
- **[filamind-iot-proxy](https://github.com/deltafabs/filamind-iot-proxy)** — the replacement for that hosted service: pairing rendezvous, ACME certificate issuer and reverse-tunnel relay, LGPL and running on your own machine.

## Arabic and right-to-left

- **[opnsense-arabic](https://github.com/AbdelmonemAwad/opnsense-arabic)** — the Arabic translation of the OPNsense 26.7 web interface, tracked against upstream so the strings don't drift between releases.
- **[opnsense-rtl](https://github.com/AbdelmonemAwad/opnsense-rtl)** — right-to-left layout for Arabic and Persian. Flipping the text direction is the easy half; tables, form flow, icon direction, menu alignment and a long tail of Bootstrap overrides are what decide whether an RTL interface is genuinely usable or merely mirrored.

The same concern runs through everything else: 19 locales in filamind-core, Arabic and English throughout filamind-ai, every OPNsense report rendered in the language of whoever has to read it, and every page the XGS driver and the plugins add to OPNsense translated into Arabic with the rest.

## cadenza

**[cadenza](https://github.com/AbdelmonemAwad/cadenza)** curates music libraries on a Synology NAS: acoustic fingerprinting to find real duplicates, metadata pulled from several sources, format conversion. It never deletes anything. Suspect files go to quarantine, because a false positive should cost you a folder, not a recording. DSM 7, x86_64.

## Not on this page

A fair amount of my work stays in private repositories: the Odoo projects built on top of the modules above, and iOS and Android applications. Ask if that is the part you need.

## What I use

Python for backends, plugins and media pipelines. C for the kernel side — the XGS drivers above all, then the Super I/O access in the fan controller and the local inference build in filamind-ai. TypeScript and Vue 3 for every FilaMind front end, React on cadenza. PHP and Volt because that is what an OPNsense interface is written in, and SCSS for its theme. Rust where a Tauri shell needs it.

Underneath: FreeBSD and its ports tree, Synology DSM 7, Docker, FastAPI, Vite, Tailwind, gettext, and GitHub Actions for CI and releases. At the hardware end: PCIe network coprocessors, SFP/SFF DOM registers, HD44780 panels through LCDproc, TMC stepper drivers, and CUDA when there is a GPU worth using.

Happy to talk about Klipper tooling, OPNsense plugins, FreeBSD, local LLM serving, or Arabic localization of infrastructure software. Questions about the XGS drivers are best asked in [the project's Discussions](https://github.com/AbdelmonemAwad/os-xgs-npu/discussions), where the answer stays for the next person.

## Recently merged

<!-- merged starts -->
- [npuep: a connection the fast path gave back is revived in place, at once from the receive path](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/492) — **os-xgs-npu**, 18 Oct
- [npuep: a connection the fast path let go is made again; install keeps a working module when a build fails (#490)](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/491) — **os-xgs-npu**, 18 Oct
- [npuep: the flow maker opens the front ports' interface entries itself](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/487) — **os-xgs-npu**, 18 Oct
- [npuep: every next hop named an empty cage - a whole link header read into a MAC's six bytes (#483)](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/486) — **os-xgs-npu**, 18 Oct
- [Flows: return a connection to the host, and a never-offloaded list](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/484) — **os-xgs-npu**, 18 Oct
- [The theme's colours as custom properties, for pages that draw with them](https://github.com/AbdelmonemAwad/os-theme-xgs/pull/4) — **os-theme-xgs**, 18 Oct
<!-- merged ends -->
