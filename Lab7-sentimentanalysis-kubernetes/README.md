# lab7-sentiment-kubernetes
Sentiment-analysis-as-a-service (SAaaS)
## Overview
In this lab, you're going to create a kubernetes cluster that provides a REST API for sentiment analysis on sentences and records them in a database. You can, if you wish, provide an alternate gRPC API following the genera outline of this lab.

You may [want to bookmark this kubernetes "cheat sheet"](https://kubernetes.io/docs/reference/kubectl/cheatsheet/).

You should complete the QwikLabs tutorials on using Docker and Kubernetes and go through [the csci 4253/5253 Kubernetes tutorial](https://github.com/cu-csci-4253-datacenter/kubernetes-tutorial) prior to starting this homework. That tutorial (and the QwikLab tutorials) shows you how to construct a simple Dockerfile, build a Docker image, push it to the Docker Hub or Google registry and then deploy it on Kubernetes. You can either use the Google cloud shell to do your work or install Docker and Kubernetes on your laptop.

You will deploy containers providing the following services.
+ rest - the REST frontend will accept API requests for analysis and handle queries concerning specific sentences. The REST worker will queue tasks to workers using `rabbitmq` messages. Full details are provided in [rest/README.md](rest/README.md).
+ worker - Worker nodes will receive work requests to analyze sentences and cache results in the Redis database. Full details are provided in [worker/README.md](worker/README.md).
+ rabbitmq - You will be provided a RabbitMQ deployment and service that acts as the rabbit-mq broker. Full details are provided in [rabbitmq/README.md](rabbitmq/README.md).
+ redis - You will be provided a Redis deployment and service to provide the redis database server. Full details are provided in [redis/README.md](redis/README.md.)

### Sentiment Analysis
The worker will use [open source sentiment analysis](https://github.com/flairNLP/flair) software. See the [worker README](worker/README.md) for more details. Our reason for turning this into a micro-service is because it takes a long time to load the sentiment analysis model.

### Setting up Kubernetes
You will need to create a Kubernetes cluster to run your code. You can either use a local install of Docker and Kubernetes or use Google Cloud's service, GKE.

Creating a cluster using GKE can done by issuing the following `gcloud` commands:
```
gcloud config set compute/zone us-central1-b
gcloud container clusters create --preemptible mykube
```
By default, this will create a 3-node cluster of `e2-medium` nodes. The `--premptible` flag drops the price (from \$0.05 per hour to \$0.01 per hour), but the nodes in your cluster will be removed within 24 hours and may be deleted at any moment. Generally, this isn't a problem, but you can omit it if you're worried. It takes 3-4 minutes to create a cluster. You can delete your cluster using  `gcloud container clusters delete mykube`.  You can use `kubectl config current-context` to see what cluster configuration you're using (e.g. local or GKE).

**Remember to delete your cluster when you're not using it.**

## Suggested Steps

You should first deploy the `rabbitmq` and `redis` provided deployments. We've provided a script `deploy-local-dev.sh` that does this and enables *port forwarding* from the corresponding services to your local host, simplifying development of your rest and worker program.

Although not explicitly required in production, we have provided [a simple python program `logs/log.py`](logs/logs.py) that connects to the debugging topic exchange as described in `rabbitmq`. You can use that to subscribe to any informational or debug messages to understand what's going on. It's useful to deploy that service as a "logs" pod (or deployment) so you can monitor the output using `kubectl logs logs-<unique id for pod>`. With port-forwarding enabled you should also be able to run it locally. If you've deployed a GKE cluster, you may also want to use the GKE logs and reporting mechanism.

Following that, you should construct the `rest` server because you can use that to test your `redis` database connection as well as connections to `rabbitmq` and your debugging interface. Lastly, start on the `worker`. We recommend that you develop your worker on your laptop because that reduces the number of times you need to build and push containers; to do this, you would port-forward the redis and rabbitmq connections to your laptop and your worker would then connect to the appropriate ports on `localhost` (see below).

When you deploy things in Kubernetes, you should use version numbers for your container images. If you're in a edit/deploy/debug cycle, your normal process to deploy new code will be to push a new container image and then delete the existing pod (rest or worker). At that point, the deployment will create a new pod. If you're using version numbers, you'll be able to insure that you're running the most recent code. You can also use the `latest` tag, but if it looks like things are using the right version, switch to version numbers.

Each subdirectory contains directions in the appropriate README file.

### Port Forwarding

While you're developing your rest and worker programs, you may want to do development on your local computer while still using the `rabbitmq` and `redis` nodes in your Kubernetes cluster. You can do this using `kubectl port-forward` for specific services which will connect a Kubernetes service to you local system (whether it's in Google's GKE or your local system). You can to that using e.g.
```
kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
kubectl port-forward --address 0.0.0.0 service/rabbitmq 5672:5672 &
```
to forward your Redis database to port 6379 on your computer and rabbitmq to local port 5672 on your computer. Then, your rest server & worker can connect to e.g. `localhost:6379` or `localhost:5672` while you test your code. The script `deploy-local-dev.sh` both deploys `rabbitq` and `redis` and then sets up port-forwarding for you.

### Sample Data
We've produced two programs `sample-requests.` and `sample-requests.sh` that make some sample requests; output `sample-requests.py` can be found in [the rest/README.md file](rest/README.md).
