import * as cdk from 'aws-cdk-lib';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { DockerImageAsset } from 'aws-cdk-lib/aws-ecr-assets';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as route53 from 'aws-cdk-lib/aws-route53';
import { Construct } from 'constructs';
import { join } from 'path';

function genid(service: string) {
	const Service = service.charAt(0).toUpperCase() + service.slice(1);
	return `Burudoza${Service}`;
}

export class BurudozaStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		// Set up the hosted zone
		const domainName = 'burudoza.com';
		// Import an existing hosted Zone
		const hostedZone =
			route53.PublicHostedZone.fromPublicHostedZoneAttributes(
				this,
				genid('hostedZone'),
				{ zoneName: domainName, hostedZoneId: 'Z034277728R677UN19XB1' }
			);

		const certificate = acm.Certificate.fromCertificateArn(
			this,
			genid('certificate'),
			process.env.ACM_ARN ?? ''
		);

		const asset = new DockerImageAsset(this, genid('dockerAsset'), {
			directory: join(__dirname, '../..'),
		});

		const image = ecs.ContainerImage.fromDockerImageAsset(asset);

		const vpc = new ec2.Vpc(this, genid('vpc'), {
			maxAzs: 2, // maximum number of availability zone
			natGateways: 0,
		});

		new ecsPatterns.ApplicationLoadBalancedFargateService(
			this,
			genid('fargateService'),
			{
				vpc,
				assignPublicIp: true, // whether the service will be assigned a public IP address.
				capacityProviderStrategies: [
					{
						capacityProvider: 'FARGATE_SPOT',
						base: 1,
						weight: 2,
					},
					{
						capacityProvider: 'FARGATE',
						base: 0,
						weight: 1,
					},
				],
				taskImageOptions: {
					image,
					containerPort: 8501,
				},
				cpu: 2048, // 2 vCPU
				memoryLimitMiB: 4096, // 4 BG of RAM
				publicLoadBalancer: true, // whether the Load Balancer will be internet-facing.
				certificate,
				listenerPort: 443, // default 80, 433 is for HTTPS
				redirectHTTP: true, // automatically create a listener on port 80 that redirects HTTP traffic to the HTTPS port.
				domainName: `app.${domainName}`,
				domainZone: hostedZone,
			}
		);
	}
}
