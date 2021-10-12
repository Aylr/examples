import argparse
import re

ap = argparse.ArgumentParser()
ap.add_argument('-f', type=str, required=True)
args = ap.parse_args()


with open(args.f, 'r') as fp:
    xml = fp.read()


xml = re.sub(r'[<]PackageReference Include="Pulumi" [^>]+[>]',
             '<ProjectReference Include="/Users/anton/pulumi/sdk/dotnet/Pulumi/Pulumi.csproj" />',
             xml)


xml = re.sub(r'[<]PackageReference Include="Pulumi.AzureNative" [^>]+[>]',
             '<ProjectReference Include="/Users/anton/pulumi-azure-native/sdk/dotnet/Pulumi.AzureNative.csproj" />',
             xml)


xml = re.sub(r'[<]PackageReference Include="Pulumi.Azure" [^>]+[>]',
             '<ProjectReference Include="/Users/anton/pulumi-azure/sdk/dotnet/Pulumi.Azure.csproj" />',
             xml)

xml = re.sub(r'[<]PackageReference Include="Pulumi.Aws" [^>]+[>]',
             '<ProjectReference Include="/Users/anton/pulumi-aws/sdk/dotnet/Pulumi.Aws.csproj" />',
             xml)


print(xml)

with open(args.f, 'w') as fp:
    fp.write(xml)
