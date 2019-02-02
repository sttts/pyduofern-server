# pyduofern-server

Based on https://github.com/gluap/pyduofern this project provides a webhook server to be called from smart home system like https://hom.ee/ to move up and down blinds.

![Calling the webhooks in Homee](https://raw.githubusercontent.com/sttts/pyduofern-server/master/homee.png)

It is run within a docker container, e.g.:

```bash
$ docker run -it --rm --name pyduofern-server --privileged -p 8080:8080 docker.io/sttts/pyduofern-server:latest --code <four-digit-code> --device /dev/ttyUSB0 -l 0.0.0.0
```

The `<four-digit-code>` (e.g. `1295`) is a code used for pairing with devices, `/dev/ttyUSB0` is the device of the Rademacher USB-Stick 70000093 (works on Mac and Linux, e.g. on a Raspberry). Default port is `8080`.

The container is multi-arch ready, supporting arm32/64 and amd64.

It serves the following API endpoints:

- `/devices/<device-id>/up` - move the blind up
- `/devices/<device-id>/down` - move the blind down.

Before using the devices with the server, they must be paired. Choose a four-digit-code (see above) and then start the container in pairing mode:

```bash
$ docker run -it --rm --name pyduofern-server --privileged docker.io/sttts/pyduofern-server:latest --code <four-digit-code> --device /dev/ttyUSB0 --pair --pair-time 120
```

After the pairing time, it will terminate.

Note: compared to https://github.com/gluap/pyduofern, pyduofern-server will not persist names of devices. It only uses the IDs, which are visible in the logs during pairing and during startup.
