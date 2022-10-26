# mftpclient
![release badge](https://badgen.net/https/ingenzivany.npkn.net/mftpclient-version) ![license MIT badge](https://badgen.net/badge/license/MIT/blue) ![tests](https://github.com/vanyingenzi/mftpclient/actions/workflows/tests.yaml/badge.svg)


## About
Minimal Python FTP client in order to allow file transfer on top of Multipath TCP (MPTCP). For a deeper read about Multipath TCP, please consult this [webpage](https://obonaventure.github.io/mmtp-book/).


## Table of Contents
- Getting Started
- Enabling MPTCP

## Getting Started 

There are no extra python dependencies needed since the client extends the CPython FTP client. 

In order to use Multipath **TCP** you have to ensure that your operating system support Multipath **TCP**. However for portability reasons if the operating system doesn't support Multipath **TCP** then the implementation falls back to a normal **TCP** connection.

## Enabling MPTCP

### Linux

Multipath **TCP** is supported in the official linux kernel starting from version 5.6. 

In order to verify is Multipath **TCP** is enabled, run the following command :

```bash
sudo sysctl -a | grep mptcp.enabled
```

The expected result should be `net.mptcp.enabled = 1`. It is possible that the output is `net.mptcp.enabled = 0`. If you want to enable it run :

```bash
sudo sysctl -w net.mptcp.enabled=1
```

Some **FTP** commands (especially `PORT`) are changed when passing through the internet by middleboxes. In order for **MTCP** to detect such changes both the client and sender have to enable the MTCP Checksum. If the checksum calculated and sent by the sender mismatch the one calculated by the receiver, then the connections fallsback to a TCP connection to preserve the established connection. More about the topic on this [page](https://obonaventure.github.io/mmtp-book/mptcp.html?highlight=ftp#coping-with-middlebox-interference). Note that for FTPS this step is not neccessary.

To enable the **MPTCP** checksum run :

```bash
sudo sysctl -w net.mptcp.checksum_enabled=1
```