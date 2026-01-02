
import os
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration


def get_pubnub_keys():
    """Just returns the PubNub keys for reference"""
    return {
        "subscribe_key": os.getenv("PUBNUB_SUB_KEY"),
        "publish_key": os.getenv("PUBNUB_PUB_KEY")
    }


# These functions are no longer needed since Access Manager is disabled
# But keep them to avoid breaking imports

def create_pi_token():
    """Placeholder"""
    return "no-token-required"


def create_web_token():
    """Placeholder"""
    return "no-token-required"