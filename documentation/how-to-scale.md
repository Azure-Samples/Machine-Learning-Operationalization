# How to scale operationalization on your ACS cluster

Operationalized models deployed on ACS clusters with Kubernetes installed can be scaled in two ways:

* You can scale the number of agent nodes in the cluster.
* You can scale the number of Kubernetes pods.
 
##  Scale the number of nodes in the cluster

The following command directly scales the agent nodes in the cluster.

    az acs scale -g <resource group> -n <cluster name> --new-agent-count <new scale>

For more information on scaling the number of nodes in the cluster, see [Scale agent nodes in a Container Service cluster](https://docs.microsoft.com/en-us/azure/container-service/container-service-scale).

## Scale the number of Kubernetes pods

Use the `-k` parameter when setting up the operationalization environment to configure one pod and install the Kubernetes CLI. You can scale the number of pods assigned to the cluster using the Azure Machine Learning CLI or the [Kubernetes dashboard] (https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/).

For more information on Kubernetes pods, see the [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) documentation.

### Scale using the Azure Machine Learning CLI

To scale the number of pods in the Kubernetes service, create the service with the `--autoscale-enabled` flag.

    az ml service create realtime --imageid [image to deploy] -n [service name] --autoscale-enabled

When using the `autoscale-enabled` flag, other autoscale parameters can be set to specify the minimum and maximum number of replicas, the scaling demand evaluation interval, and the target utilization of replicas time. For more information on using the autoscale parameters, see the [Model Management Command Line Interface Reference](aml-cli-reference.md) documentation.

### Scale using the Kubernetes dashboard

The command to start the Kubernetes dashboard web interface is the same on both Windows and Linux:

    kubectl proxy

On Windows, the Kubernetes install location is not automatically added to the path. First navigate to the install folder:
    
    c:\users\<user name>\bin

Once you run the command, you should see the following informational message:

    Starting to serve on 127.0.0.1:8001

If the port is already in use, you see a message similar to the following example:

    F0612 21:49:22.459111   59621 proxy.go:137] listen tcp 127.0.0.1:8001: bind: address already in use

You can specify an alternate port number using the *--port* parameter.

    kubectl proxy --port=8010
    Starting to serve on 127.0.0.1:8010

Once you have started the dashboard server, open a browser and enter the following URL:

    127.0.0.1:<port number>/ui

From the dashboard main screen, click **Deployments** on the left navigation bar. If the navigation pane does not display, select this icon ![Menu consisting of three short horizontal lines](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/images/hamburger-icon.jpg) on the upper left.

Locate the deployment to modify and click this icon ![Menu icon consisting of three vertical dots](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/images/kebab-icon.jpg) on the right and then click **View/edi YAML**.

On the Edit deployment screen, locate the *spec* node, modify the *replicas* value, and click **Update**.
