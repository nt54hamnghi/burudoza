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

		const vpc = new ec2.Vpc(this, genid('vpc'), {
			maxAzs: 2, // maximum number of availability zone, default is All
		});

		const cluster = new ecs.Cluster(this, genid('cluster'), {
			vpc: vpc,
		});

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

		new ecsPatterns.ApplicationLoadBalancedFargateService(
			this,
			genid('fargateService'),
			{
				assignPublicIp: true,
				cluster,
				cpu: 4096, // 4 vCPU
				taskImageOptions: {
					image,
					containerPort: 8501,
				},
				memoryLimitMiB: 8192, // 8 BG of RAM
				publicLoadBalancer: true,
				certificate: certificate,
				listenerPort: 443, // default 80, 433 is for HTTPS
				domainName: `app.${domainName}`,
				domainZone: hostedZone,
			}
		);
	}
}
