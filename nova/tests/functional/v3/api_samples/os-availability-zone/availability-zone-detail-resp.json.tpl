{
    "availabilityZoneInfo": [
        {
            "hosts": {
                "consoleauth": {
                    "nova-consoleauth": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                },
                "cert": {
                    "nova-cert": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                },
                "conductor": {
                    "nova-conductor": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                },
                "cells": {
                    "nova-cells": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                },
                "scheduler": {
                    "nova-scheduler": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                },
                "network": {
                    "nova-network": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                }
            },
            "zoneName": "internal",
            "zoneState": {
                "available": true
            }
        },
        {
            "hosts": {
                "compute": {
                    "nova-compute": {
                        "active": true,
                        "available": true,
                        "updated_at": %(strtime_or_none)s
                    }
                }
            },
            "zoneName": "nova",
            "zoneState": {
                "available": true
            }
        }
    ]
}
