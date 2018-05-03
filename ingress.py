#!/usr/local/bin/python

from kubernetes import client, config
import json
import time
import os

def getIngress():
    kubeConfig = '/tmp/config'
    ingress = {}
    ingressList = []
    global config

    if os.path.exists(kubeConfig):
        config.load_kube_config(kubeConfig)
        print '\n Using local Kube config for API authentication/authorization...\n'
    else:
        tokenFile = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        caFile = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
        with open (tokenFile, "r") as apiToken:
            token = apiToken.read()
        apiToken.close
        config = client.Configuration()
        config.host = "https://kubernetes.default.svc.cluster.local"
        config.api_key = {"authorization": "Bearer " + token}
        config.ssl_ca_cert = caFile
        client.Configuration.set_default(config)
        print '\n Using cluster service account token for API authentication/authorization...\n'

    v1beta1 = client.ExtensionsV1beta1Api()

    response = json.loads(v1beta1.list_ingress_for_all_namespaces(_preload_content=False))
    for item in response['items']:
        ingress['name'] = item['metadata']['name']
        ingress['namespace'] = item['metadata']['namespace']
        for rule in item['spec']['rules']:
            ingress['host'] = rule['host']
            for path in rule['http']['paths']:
                ingress['serviceName'] = path['backend']['serviceName']
        ingressList.append(ingress)
    return ingressList

if __name__ == "__main__":
    getIngress()