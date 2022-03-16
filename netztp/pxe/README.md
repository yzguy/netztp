# PXE

### DHCP Configuration

DHCP is configured to detect if the machine is BIOS or UEFI, and if it's iPXE or not.
If it's not iPXE it will go through an extra step that loads iPXE, which gives us a lot more power/flexibility.

```
If BIOS
  If iPXE
    Request boot from TFTP
  Else
    Request iPXE from TFTP
```

```
class "BIOS" {
   match if substring(option vendor-class-identifier, 0, 20) = "PXEClient:Arch:00000";
   if exists user-class and option user-class = "iPXE" {
      filename "boot";
   } else {
      filename = "undionly.kpxe";
   }
}

class "UEFI" {
   match if substring(option vendor-class-identifier, 0, 20) = "PXEClient:Arch:00007";
   if exists user-class and option user-class = "iPXE" {
      filename "boot";
   } else {
      filename = "ipxe.efi";
   }
}

next-server 192.168.221.2;
```

### TFTP Configuration

Our server just runs tftp-hpa, nothing crazy. In the root of the TFTP servers we have 3 files

```
boot
ipxe.efi
undionly.kpxe
```

2 are the various iPXE bootloaders, and the other is a text file that iPXE will eventually request

This text file contains simple a command to tell iPXE to request a boot configuration from NetZTP and pass it's MAC address.

```
#!ipxe

chain http://ztp.yzguy.io/pxe/boot?mac=${net0/mac}
```

### NetZTP PXE Configurations

In order to decouple the cloud-init/ignition configuration from NetZTP, the configurations are stored in a different repository, and on boot NetZTP will clone the repository. This requires NetZTP to have a deploy key from GitHub so it can do the clone.

Additionally, there is a URL endpoint to force NetZTP to pull the latest configurations from Git at `/pxe/refresh`, with an optional URL parameter of `branch` to tell it to pull the configurations from a specific branch. This is useful for quickly testing a configuration live before it's merged.

Two environment variables are needed to be configured for this functionality

```
GITHUB_TOKEN
PXE_CONFIG_REPO
```