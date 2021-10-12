# Compute example translation progress.

import json
import subprocess as sp
import sys
import yaml


def increment(d, k):
    d[k] = d.get(k, 0) + 1


def language(yaml_file):
    with open(yaml_file, 'r') as fp:
        d = yaml.load(fp, Loader=yaml.FullLoader)

    x = d['runtime']
    if type(x) == dict:
        return x['name']

    return x


def is_cs_like(d):
    return '-cs-' in d


def read_done_configs():
    with open('done.json', 'r') as fp:
        done_list = json.load(fp)
    return set(done_list)


def write_done_configs(done_set):
    with open('done.json', 'w') as fp:
        obj = sorted([x for x in done_set])
        json.dump(obj, fp, indent=True)


def collect_stats():
    done_configs = read_done_configs() | DONE

    all_git_files = [x for x in sp.check_output('git ls-files', shell=True).decode('utf-8').split('\n') if x]
    pulumi_configs = [x for x in all_git_files if 'Pulumi' in x]

    stats = {'python_done': 0, 'go_done': 0, 'nodejs_done': 0, 'dotnet_done': 0}

    for cfg in pulumi_configs:
        is_done = cfg in done_configs
        lang = language(cfg)
        increment(stats, f'total')
        increment(stats, f'{lang}_total')
        if is_done:
            increment(stats, f'done')
            increment(stats, f'{lang}_done')
        else:
            key = f'{lang}_next'
            prev = stats.get(key, None)
            if prev is None or cfg < prev:
                stats[key] = cfg

    return stats


DONE = set([
    'aws-ts-eks-migrate-nodegroups/Pulumi.yaml',
    'aws-ts-eks-hello-world/Pulumi.yaml',
    'aws-ts-eks-distro/Pulumi.yaml',
    'aws-ts-ecs-anywhere/Pulumi.yaml',
    'aws-ts-ec2-provisioners/Pulumi.yaml',
    'aws-ts-containers/Pulumi.yaml',
    'aws-ts-assume-role/create-role/Pulumi.yaml',
    'aws-ts-assume-role/assume-role/Pulumi.yaml',
    'aws-ts-appsync/Pulumi.yaml',
    'aws-ts-apigatewayv2-http-api/Pulumi.yaml',
    'aws-ts-apigatewayv2-http-api-quickcreate/Pulumi.yaml',
    'aws-ts-apigateway/Pulumi.yaml',
    'aws-ts-apigateway-lambda-serverless/Pulumi.yaml',
    'aws-ts-apigateway-auth0/Pulumi.yaml',
    'aws-ts-airflow/Pulumi.yaml',
    'aws-stackreference-architecture/networking/Pulumi.yaml',  ## had getAvailabilityZones? but availabilityZoneNames: string[]
    'aws-stackreference-architecture/database/Pulumi.yaml',
    'aws-stackreference-architecture/application/Pulumi.yaml',
    'aws-pern-voting-app/Pulumi.yaml',
    'aws-native-ts-stepfunctions/Pulumi.yaml',
    'aws-native-ts-s3-folder/Pulumi.yaml',
    'aws-native-ts-ecs/Pulumi.yaml',
    'aws-js-webserver/Pulumi.yaml',
    'aws-js-webserver-component/Pulumi.yaml',
    'aws-js-sqs-slack/Pulumi.yaml',
    'aws-js-s3-folder/Pulumi.yaml',
    'aws-js-s3-folder-component/Pulumi.yaml',
    'aws-js-containers/Pulumi.yaml',
    'testing-unit-py/Pulumi.yaml',
    'testing-integration-py/Pulumi.yaml',
    'policy-packs/kubernetes-python/PulumiPolicy.yaml',
    'policy-packs/gcp-python/PulumiPolicy.yaml',
    'policy-packs/azure-python/PulumiPolicy.yaml',
    'policy-packs/aws-python/PulumiPolicy.yaml',
    'openstack-py-webserver/Pulumi.yaml',
    'misc/benchmarks/py-many-resources/Pulumi.yaml',
    'libvirt-py-vm/Pulumi.yaml',
    'kubernetes-py-nginx/Pulumi.yaml',
    'kubernetes-py-jenkins/Pulumi.yaml',
    'kubernetes-py-guestbook/simple/Pulumi.yaml',
    'kubernetes-py-guestbook/components/Pulumi.yaml',
    'gcp-py-webserver/Pulumi.yaml',
    'gcp-py-serverless-raw/Pulumi.yaml',
    'gcp-py-network-component/Pulumi.yaml',
    'gcp-py-instance-nginx/Pulumi.yaml',
    'gcp-py-gke/Pulumi.yaml',
    'gcp-py-functions/Pulumi.yaml',
    'gcp-py-cloudrun-cloudsql/Pulumi.yaml',
    'equinix-metal-py-webserver/Pulumi.yaml',
    'docker-py-multi-container-app/Pulumi.yaml',
    'digitalocean-py-loadbalanced-droplets/Pulumi.yaml',
    'digitalocean-py-k8s/Pulumi.yaml',
    'classic-azure-py-webserver-component/Pulumi.yaml',
    'classic-azure-py-vm-scaleset/Pulumi.yaml',
    'classic-azure-py-msi-keyvault-rbac/Pulumi.yaml',
    'classic-azure-py-hdinsight-spark/Pulumi.yaml',
    'classic-azure-py-arm-template/Pulumi.yaml',
    'classic-azure-py-aks-multicluster/Pulumi.yaml',
    'azure-py-webserver/Pulumi.yaml',
    'azure-py-virtual-data-center/Pulumi.yaml',
    'azure-py-synapse/Pulumi.yaml',
    'azure-py-static-website/Pulumi.yaml',
    'azure-py-minecraft-server/Pulumi.yaml',
    'azure-py-cosmosdb-logicapp/Pulumi.yaml',
    'azure-py-call-azure-sdk/Pulumi.yaml',
    'azure-py-appservice/Pulumi.yaml',  # needs testing
    'azure-py-appservice-docker/Pulumi.yaml',
    'azure-py-aks/Pulumi.yaml',
    'azure-py-aks-multicluster/Pulumi.yaml',
    'azure-py-aks-helm/Pulumi.yaml',
    'azure-py-aci/Pulumi.yaml',
    'aws-ts-vpc-with-ecs-fargate-py/ecs-fargate-python/Pulumi.yaml',
    'aws-py-wordpress-fargate-rds/Pulumi.yaml',
    'aws-py-webserver/Pulumi.yaml',
    'aws-py-voting-app/Pulumi.yaml',
    'aws-py-stepfunctions/Pulumi.yaml',
    'aws-py-static-website/Pulumi.yaml', # getZone prob ok
    'aws-py-stackreference/team/Pulumi.yaml',
    'aws-py-stackreference/department/Pulumi.yaml',
    'aws-py-stackreference/company/Pulumi.yaml',
    'aws-py-slackbot/Pulumi.yaml',
    'aws-py-serverless-raw/Pulumi.yaml', # similarly would not benefit
    'aws-py-s3-folder/Pulumi.yaml',
    'aws-py-resources/Pulumi.yaml',
    'aws-py-eks/Pulumi.yaml',
    'aws-py-fargate/Pulumi.yaml',
    'aws-py-ecs-instances-autoapi/py-ecs-instance/Pulumi.yaml', # has functions but did not benefit
    'aws-py-ec2-provisioners/Pulumi.yaml',
    'aws-py-dynamicresource/Pulumi.yaml',
    'aws-py-assume-role/create-role/Pulumi.yaml',
    'aws-py-assume-role/assume-role/Pulumi.yaml',
    'aws-py-appsync/Pulumi.yaml',
    'aws-py-apigatewayv2-http-api-quickcreate/Pulumi.yaml',
    'aws-py-apigateway-lambda-serverless/Pulumi.yaml',
    'aws-django-voting-app/Pulumi.yaml',
    'testing-unit-go/Pulumi.yaml', ## SKIP awkward GetAmiIdsx
    'azure-go-appservice-docker/Pulumi.yaml', ## same azure-native
    'azure-go-aks/Pulumi.yaml',       ## same azure-native
    'azure-go-aks-helm/Pulumi.yaml',  ## could use the update, but azure-native --> disableFunctionOutputVersions=true
    'misc/benchmarks/go-many-resources/Pulumi.yaml',
    'kubernetes-go-helm-wordpress/Pulumi.yaml',
    'kubernetes-go-guestbook/simple/Pulumi.yaml',
    'kubernetes-go-guestbook/components/Pulumi.yaml',
    'kubernetes-go-exposed-deployment/Pulumi.yaml',
    'kubernetes-go-configmap-rollout/Pulumi.yaml',
    'gcp-go-webserver/Pulumi.yaml',
    'gcp-go-instance/Pulumi.yaml',
    'gcp-go-gke/Pulumi.yaml',
    'gcp-go-functions/Pulumi.yaml',
    'gcp-go-functions-raw/Pulumi.yaml',
    'crd2pulumi-crontabs/kubernetes-go-crontabs/Pulumi.yaml',
    'classic-azure-go-webserver-component/Pulumi.yaml',
    'classic-azure-go-aks-multicluster/Pulumi.yaml',
    'azure-go-static-website/Pulumi.yaml',
    'azure-go-call-azure-sdk/Pulumi.yaml',
    'azure-go-aks-multicluster/Pulumi.yaml',
    'azure-go-aci/Pulumi.yaml',
    'aws-go-webserver/Pulumi.yaml',
    'aws-go-slackbot/Pulumi.yaml',
    'aws-go-s3-folder/Pulumi.yaml',
    'aws-go-s3-folder-component/Pulumi.yaml',
    'aws-go-resources/Pulumi.yaml',
    'aws-go-lambda/Pulumi.yaml',
    'aws-go-lambda-gateway/Pulumi.yaml',
    'aws-go-fargate/Pulumi.yaml',
    'aws-go-eks/Pulumi.yaml',
    'aws-go-console-slack-notification/Pulumi.yaml',
    'aws-go-assume-role/create-role/Pulumi.yaml',
    'aws-go-assume-role/assume-role/Pulumi.yaml',
    'aws-go-appsync/Pulumi.yaml',
    'testing-unit-fs-mocks/Pulumi.yaml',
    'testing-unit-cs/Pulumi.yaml',
    'misc/benchmarks/cs-many-resources/Pulumi.yaml',
    'classic-azure-fs-appservice/Pulumi.yaml',
    'classic-azure-fs-aks/Pulumi.yaml',
    'classic-azure-fs-aci/Pulumi.yaml',
    'aws-fs-s3-folder/Pulumi.yaml',
    'aws-fs-lambda-webserver/pulumi/Pulumi.yaml',
    'aws-cs-assume-role/assume-role/Pulumi.yaml',
    'aws-cs-assume-role/create-role/Pulumi.yaml',
    'aws-cs-eks/Pulumi.yaml',
    'aws-cs-fargate/Pulumi.yaml',
    'aws-cs-lambda/pulumi/Pulumi.yaml',
    'aws-cs-s3-folder/Pulumi.yaml',
    'aws-cs-webserver/Pulumi.yaml',
    'azure-cs-aci/Pulumi.yaml',
    'azure-cs-aks-cosmos-helm/Pulumi.yaml',
    'azure-cs-aks-helm/Pulumi.yaml',
    'azure-cs-aks-multicluster/Pulumi.yaml',
    'azure-cs-aks/Pulumi.yaml',
    'azure-cs-appservice-docker/Pulumi.yaml',
    'azure-cs-appservice/Pulumi.yaml',
    'azure-cs-call-azure-api/Pulumi.yaml',
    'azure-cs-cosmosdb-logicapp/Pulumi.yaml',
    'azure-cs-credential-rotation-one-set/Pulumi.yaml',
    'azure-cs-functions/Pulumi.yaml',
    'azure-cs-net5-aks-webapp/Pulumi.yaml',
    'azure-cs-synapse/Pulumi.yaml',
    'classic-azure-cs-msi-keyvault-rbac/Pulumi.yaml',
    'classic-azure-cs-vm-scaleset/Pulumi.yaml',
    'classic-azure-cs-webserver/Pulumi.yaml',
    'gcp-cs-gke/Pulumi.yaml',

    # no cs invokes here
    'azure-cs-static-website/Pulumi.yaml',
    'classic-azure-cs-botservice/Pulumi.yaml',
    'classic-azure-cs-cosmosapp-component/Pulumi.yaml',
    'digitalocean-cs-k8s/Pulumi.yaml',
    'digitalocean-cs-loadbalanced-droplets/Pulumi.yaml',
    'docker-cs-multi-container-app/Pulumi.yaml',
    'gcp-cs-functions/Pulumi.yaml',
    'kubernetes-cs-guestbook/components/Pulumi.yaml',
    'kubernetes-cs-guestbook/simple/Pulumi.yaml',
    'testing-unit-cs-mocks/Pulumi.yaml',
])


if __name__ == '__main__':
    stats = collect_stats()

    if 'next-nodejs' in sys.argv and 'nodejs_next' in stats:
        n = stats['nodejs_next']
        write_done_configs(read_done_configs() | set([n]))
        print(f'Added {n} done.json')
        stats = collect_stats()

    print(f'Done {stats["done"]}/{stats["total"]}')
    print(f'.NET {stats["dotnet_done"]}/{stats["dotnet_total"]}')
    print(f'Py   {stats["python_done"]}/{stats["python_total"]}')
    print(f'Go   {stats["go_done"]}/{stats["go_total"]}')
    print(f'Node {stats["nodejs_done"]}/{stats["nodejs_total"]}')

    print('')
    for lang in ['dotnet', 'python', 'go', 'nodejs']:
        n = stats.get(f'{lang}_next', None)
        if n:
            print(f'{lang} next:\t{n}')
