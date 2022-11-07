from flask import jsonify, request
from src.models.Blockchain import BlockChain
import requests
from uuid import uuid4
from urllib.parse import urlparse

def routes(app, blockchain):
    pass