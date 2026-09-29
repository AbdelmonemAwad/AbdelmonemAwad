<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img src="assets/banner-light.svg" alt="Abdelmonem Awad — self-hosted tools for machines that run unattended" width="100%">
</picture>

Hi, I'm Abdelmonem. I build self-hosted software for hardware that is supposed to look after itself — and, lately, drivers for hardware that refuses to be driven at all. Alongside that: a control suite for Klipper 3D printers, plugins for OPNsense firewalls, local LLM serving on Synology hardware, Odoo modules, and iOS and Android apps.

Most of it is Python and TypeScript. Almost all of it ships in Arabic as well as English, because the people running this hardware do not all read English.

## os-xgs-npu — Sophos XGS on FreeBSD

Install OPNsense on a Sophos XGS 136 and it boots to a working firewall with **no network interfaces at all**. The appliance looks like one computer and is two: an x86 host, and a Marvell CN9131 coprocessor behind a PCIe endpoint that owns every front port. Sophos ships Linux drivers only, so the usual verdict on this hardware is e-waste.

It isn't. The coprocessor is a whole computer, booting its own Linux from its own eMMC, waiting to be told a host is present. **[os-xgs-npu](https://github.com/AbdelmonemAwad/os-xgs-npu)** is the FreeBSD kernel module that tells it — written against registers no vendor documents.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/npu-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/npu-light.svg">
  <img src="assets/npu-light.svg" alt="How the driver reaches the front ports: OPNsense host, npuep module, PCIe BAR, one queue pair, the CN9131 coprocessor, fourteen front ports" width="100%">
</picture>

All fourteen front ports carry traffic in both directions, as ordinary FreeBSD interfaces created at boot with nothing typed. Twelve are verified port by port with loopback cables rather than a single ARP exchange; the two SFP cages need fibre I don't have. The port order came out of a disassembly, and the loopback run confirmed it — a frame leaving `npup10` arrived on `npup9`, exactly where the disassembled table said it would.

The result that matters for a firewall: while transmitting out of each port in turn, the sending port's own counter never moved. The coprocessor's internal switch does not forward between front ports behind the host's back, so `pf` is the only forwarder. If it did, traffic would pass between two ports without the firewall ever seeing it.

On an XGS 3300 — Cavium OCTEON TX, different silicon entirely — the host-to-coprocessor management link is up and carries IP; its twelve front ports are untouched. Four further families are described from vendor tables with no hardware here at all, and every row says which is which.

It is experimental, and the repository says so loudly: writing to an undocumented PCIe coprocessor from a kernel module of my own making has wedged the bench hard enough to need a power cycle by hand, more than once. Run it on nothing you depend on.

## FilaMind — Klipper and Moonraker

[FilaMind](https://github.com/filamind-app) is an open-source, self-hosted suite for makers running Klipper and Moonraker. Most of my commits over the past year went here.

- **[filamind-core](https://github.com/filamind-app/filamind-core)** — the TypeScript foundation the rest is built on: a Moonraker client, a session orchestrator, a fail-closed write arbiter so two front ends can never fight over the same printer, and i18n for 19 locales.
- **[filamind-flow](https://github.com/filamind-app/filamind-flow)** — the control panel: firmware flashing, input shaping, TMC motor-driver tooling. Python and FastAPI behind Vue 3, built one widget at a time so each piece can be adopted on its own.
- **[filamind-screen](https://github.com/filamind-app/filamind-screen)** — the on-printer touch interface, same core, wrapped as a desktop app with Tauri 2.
- **[filamind-3d](https://github.com/filamind-app/filamind-3d)** — the web control UI on top of the core. Vue 3, Vite and Tailwind over a lean FastAPI host.
- **[filamind-ai](https://github.com/filamind-app/filamind-ai)** — private AI for a Synology NAS: local LLM chat with optional cloud fallback, multi-user, an OpenAI-compatible API, and a full interface in both Arabic and English. Runs on a DVA 3221 with its CUDA GPU, or a DS1821+ on CPU.
- **[filamind-setup](https://github.com/filamind-app/filamind-setup)** — one installer engine behind two front ends, a CLI and a widget inside flow.

## OPNsense plugins

Four plugins, BSD-2 licensed like the platform itself and packaged as FreeBSD ports.

- **[os-linkhealth](https://github.com/AbdelmonemAwad/os-linkhealth)** — watches every physical port and names the cable or transceiver that is going bad, by the label printed on the chassis rather than the interface name. It reads the DOM registers on the transceivers, so the warning arrives before the link actually drops.
- **[os-netreport](https://github.com/AbdelmonemAwad/os-netreport)** — scheduled network reports by email, and an alert the first time an unknown device shows up. Each report is written in whichever language the GUI is set to.
- **[os-frontpanel](https://github.com/AbdelmonemAwad/os-frontpanel)** — drives the LCD and buttons built into an appliance's front panel through LCDproc, with the screens and their timing set from the GUI instead of a config file on disk.
- **[os-fanctl](https://github.com/AbdelmonemAwad/os-fanctl)** — fan control and every readable temperature sensor, for repurposed appliances whose fan curve left with the vendor firmware. Talks to the Super I/O chip directly.

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

The same concern runs through everything else: 19 locales in filamind-core, Arabic and English throughout filamind-ai, and every OPNsense report rendered in the language of whoever has to read it.

## cadenza

**[cadenza](https://github.com/AbdelmonemAwad/cadenza)** curates music libraries on a Synology NAS: acoustic fingerprinting to find real duplicates, metadata pulled from several sources, format conversion. It never deletes anything. Suspect files go to quarantine, because a false positive should cost you a folder, not a recording. DSM 7, x86_64.

## Not on this page

A fair amount of my work stays in private repositories: the Odoo projects built on top of the modules above, and iOS and Android applications. Ask if that is the part you need.

## What I use

Python for backends, plugins and media pipelines. TypeScript and Vue 3 for every FilaMind front end, React on cadenza. PHP and Volt because that is what an OPNsense interface is written in. Rust where a Tauri shell needs it, and C for the kernel-side work: the XGS driver, the Super I/O access in the fan controller, and the local inference build in filamind-ai.

Underneath: FreeBSD and its ports tree, Synology DSM 7, Docker, FastAPI, Vite, Tailwind, gettext, and GitHub Actions for CI and releases. At the hardware end: SFP/SFF DOM registers, HD44780 panels through LCDproc, TMC stepper drivers, and CUDA when there is a GPU worth using.

Happy to talk about Klipper tooling, OPNsense plugins, FreeBSD, local LLM serving, or Arabic localization of infrastructure software.

## Recently shipped

<!-- releases starts -->
- [**cadenza** v2.11.4-0036](https://github.com/AbdelmonemAwad/cadenza/releases/tag/v2.11.4-0036) — 15 Sep 2026
- [**filamind-3d** v0.2.1](https://github.com/filamind-app/filamind-3d/releases/tag/v0.2.1) — 23 Jul 2026
- [**filamind-screen** v0.18.1](https://github.com/filamind-app/filamind-screen/releases/tag/v0.18.1) — 23 Jul 2026
- [**filamind-core** v0.1.6](https://github.com/filamind-app/filamind-core/releases/tag/v0.1.6) — 23 Jul 2026
- [**filamind-flow** v1.25.2](https://github.com/filamind-app/filamind-flow/releases/tag/v1.25.2) — 23 Jul 2026
- [**filamind-ai** v1.4.1](https://github.com/filamind-app/filamind-ai/releases/tag/v1.4.1) — 30 May 2026
<!-- releases ends -->

<!-- Fill this in and remove the comment markers to show it on the profile:
[![Email](https://img.shields.io/badge/Email-0D1117?style=flat-square&logo=gmail&logoColor=F97316)](mailto:YOUR_EMAIL)
-->
