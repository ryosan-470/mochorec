#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mochorec command line tools
import mochorec.niconico as nico


def main():
    n = nico.Niconico()
    n.login()
    print("[+] Login success")

    status = n.getplayerstatus("lv272216525")
    print(status)


if __name__ == "__main__":
    main()
