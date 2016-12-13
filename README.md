# NuxSFM 2.0 pacman X86_64 build scripts

## About NuxSFM

NuxSFM is an Arch Linux X86_64 ~~Nvidia optimized base~~ distribution dedicated to Structure From Motion (SFM) and 3D Photogrammetry. The goal of NuxSFM is to provide a free (opensource) and suitable test or development platform for developpers and users like me who are interested in testing computer vision developments around 3D reconstruction. You can pickup and tweak NuxSFM code or scripts for any purposes. BUT keep in mind that it relies on other open (or closed) GNU/GPL/MIT/... and so on code which have their own scope of use. So please pay attention to licences, terms and conditions of use of those codes. NuxSFM includes individual details of thoses licences and terms in its binaries and building scripts. Please read them if you have any doubt.

Originally started by Pierre (@pyp_22), this repository is a quick and easy way to use open source libraries for photogrammetry.

## Usage

Add the following repo to your pacman.conf 

```
[archlinuxfr]
SigLevel = Optional TrustAll
Server = http://repo.archlinux.fr/$arch

[nuxsfm]
SigLevel = Optional TrustAll
Server = http://stephane-lb.github.io/NuxSFM/$arch
```

Synchronize and update your local database :

```
pacman -Ssyu
```

Install the packages you want (for example):

```
pacman -S openMVG
```


## Licence

See LICENCE.
