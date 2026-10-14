<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img src="assets/banner-light.svg" alt="Abdelmonem Awad — self-hosted tools for machines that run unattended" width="100%">
</picture>

Hi, I'm Abdelmonem. I build self-hosted software for hardware that is supposed to look after itself — and, lately, drivers for hardware that refuses to be driven at all. Alongside that: a control suite for Klipper 3D printers, plugins for OPNsense firewalls, local LLM serving on Synology hardware, Odoo modules, and iOS and Android apps.

Most of it is Python, TypeScript and C. Almost all of it ships in Arabic as well as English, because the people running this hardware do not all read English.

## os-xgs-npu — reclaiming a family of firewalls

Install OPNsense on a Sophos XGS and it boots to a working firewall with **no network interfaces at all**. The appliance looks like one computer and is two: an x86 host, and a coprocessor behind a PCIe endpoint that owns every front port. Sophos ships drivers for Linux and for its own OS only, so when support lapses the usual verdict on the hardware is e-waste.

**[os-xgs-npu](https://github.com/AbdelmonemAwad/os-xgs-npu)** is a pair of FreeBSD kernel modules, written against registers no vendor documents, that hand those ports back. The XGS line spans six coprocessor families; get the protocol right for one and every assembly in it becomes a general-purpose FreeBSD router. Two answer now, on silicon that shares nothing.

| Family | Assemblies | Coprocessor | State |
| :--- | :--- | :--- | :--- |
| **OCTEON TX** | AMDA0202 (XGS 3300) | Cavium CN83XX | **Working** — twelve of twelve front ports, with IPsec and flow offload on the coprocessor |
| **ARMADA** | AMDA0201 (XGS 126, 136), 0200, 0208, 0224 | Marvell CN9131 | **Working** — fourteen of fourteen front ports on the XGS 136 |
| **OCTEON TX2** | AMDA0203, 0204, 0225, 0228 | Cavium OCTEON TX2 | Described from the vendor's binaries; no hardware here |
| **OCTEON TX2 98XX** | AMDA0205, 0226 | Cavium OCTEON TX2 98XX | Described from the vendor's binaries; no hardware here |
| **TOPAZ**, **GR** | Atom boards | none | No coprocessor exists — nothing to drive |

> **The repository is much younger than the work in it.** Months of reverse engineering, measurement
> and dead ends on real appliances came before any of it went public, and one of the faults it closes
> had been open for eighteen of them.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/octeon-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/octeon-light.svg">
  <img src="assets/octeon-light.svg" alt="The Cavium path: OPNsense host, eight virtual functions, handshake and facilities, eight SDP rings, the CN83XX fast path, twelve front ports" width="100%">
</picture>

**The ports.** On the XGS 3300 all twelve are ordinary FreeBSD interfaces, one of them carrying the appliance's WAN, and a gigabit port measures at line rate: 1,023 Mbit/s, with everything the driver offered beyond that refused at the coprocessor's own egress queue and counted there. On the XGS 136 all fourteen are, and the coprocessor's internal switch was shown not to forward between front ports behind the host's back — so `pf` stays the only forwarder, which is what a firewall needs.

**The offload.** An IPsec association that strongSwan installs through OPNsense lands on the coprocessor's crypto engine with nothing typed, and a connection inside the tunnel can join the flow table with it, so the host leaves the data path. On a real tunnel between two appliances that is 951 Mbit/s down and 946 up — but the kernel's own cipher reaches much the same rate, and the repository says so. **What the offload buys is the host's processor**: most of a core at a gigabit against a few hundredths of one, with the flow table taking the host out of 99.6 per cent of a connection's frames. AES-GCM and AES-CBC with an HMAC, IPv4 and IPv6 inside and out, NAT traversal and replay windows up to 4,096 are all taken; GCM-8 and GCM-12, transport mode and inbound extended sequence numbers stay with the kernel. It is off by default.

**Getting it onto an appliance.** It installs as an OPNsense plugin with its own status and settings pages, and **[xgs-image-builder](https://github.com/AbdelmonemAwad/xgs-image-builder)** builds a bootable image with the driver already in it from [a page in the browser](https://abdelmonemawad.github.io/xgs-image-builder/) — though nothing built that way has been booted on an appliance yet.

**How it is kept honest.** On the way to the last hop alone, ten published claims were withdrawn and nineteen attempts recorded as not working, each in the place it was made and counted on [a page of its own](https://github.com/AbdelmonemAwad/os-xgs-npu/blob/main/docs/the-road.md). Every number comes with how it was taken in [the measurements](https://github.com/AbdelmonemAwad/os-xgs-npu/tree/main/docs/measurements), and the rest is in [the documentation](https://github.com/AbdelmonemAwad/os-xgs-npu/tree/main/docs). The integrity soaks stand at 2,391 GiB carried over TLS with not a byte changed. It is still experimental — it has wedged the bench hard enough to need a power cycle by hand, more than once — so read the notice at the top of the repository before running any of it: at times it says not to.

<details>
<summary>The Marvell path, drawn the same way</summary>

<br>

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

Four plugins, BSD-2 licensed like the platform itself and packaged as FreeBSD ports.

- **[os-linkhealth](https://github.com/AbdelmonemAwad/os-linkhealth)** — watches every physical port and names the cable or transceiver that is going bad, by the label printed on the chassis rather than the interface name. It reads the DOM registers on the transceivers, so the warning arrives before the link actually drops.
- **[os-netreport](https://github.com/AbdelmonemAwad/os-netreport)** — scheduled network reports by email, and an alert the first time an unknown device shows up. Each report is written in whichever language the GUI is set to.
- **[os-frontpanel](https://github.com/AbdelmonemAwad/os-frontpanel)** — drives the LCD and buttons built into an appliance's front panel through LCDproc, with the screens and their timing set from the GUI instead of a config file on disk.
- **[os-fanctl](https://github.com/AbdelmonemAwad/os-fanctl)** — fan control and every readable temperature sensor, for repurposed appliances whose fan curve left with the vendor firmware. Talks to the Super I/O chip directly.

Three of them now know the Sophos XGS appliances above — port labels and port identification through the coprocessor, temperature and fan readings from the board and from the coprocessor, the 3300's two-line front panel — so a reclaimed box gets more back than its ports.

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

Python for backends, plugins and media pipelines. C for the kernel side — the XGS drivers above all, then the Super I/O access in the fan controller and the local inference build in filamind-ai. TypeScript and Vue 3 for every FilaMind front end, React on cadenza. PHP and Volt because that is what an OPNsense interface is written in. Rust where a Tauri shell needs it.

Underneath: FreeBSD and its ports tree, Synology DSM 7, Docker, FastAPI, Vite, Tailwind, gettext, and GitHub Actions for CI and releases. At the hardware end: PCIe network coprocessors, SFP/SFF DOM registers, HD44780 panels through LCDproc, TMC stepper drivers, and CUDA when there is a GPU worth using.

Happy to talk about Klipper tooling, OPNsense plugins, FreeBSD, local LLM serving, or Arabic localization of infrastructure software.

## Recently merged

<!-- merged starts -->
- [xgs/status: report the ARMADA coprocessor too, not only OCTEON TX](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/397) — **os-xgs-npu**, 14 Oct
- [npuep: accept a decrypt association, the engine decrypts inbound ESP (step 5, slice 3)](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/396) — **os-xgs-npu**, 14 Oct
- [npuep: SA_ADD - the crypto engine accepts an association (step 5, slice 2)](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/395) — **os-xgs-npu**, 14 Oct
- [npuep: advertise the kernel's IPsec offload contract (step 5, slice 1)](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/394) — **os-xgs-npu**, 14 Oct
- [npuflow: share one next-hop entry between flows that leave the same way](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/393) — **os-xgs-npu**, 14 Oct
- [npuflow: the firewall-revision barrier (step 4, slice 4)](https://github.com/AbdelmonemAwad/os-xgs-npu/pull/392) — **os-xgs-npu**, 14 Oct
<!-- merged ends -->
