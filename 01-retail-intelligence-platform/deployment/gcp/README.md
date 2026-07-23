# GCP Deployment — Cloud Run

## Architecture

```text
Browser
  -> retail-intelligence-web (Cloud Run, public)
       static React build with immutable API origin
  -> retail-intelligence-api (Cloud Run, public GET API)
       validated repository evidence packaged read-only in the image

Cloud Build -> Artifact Registry -> immutable Cloud Run revisions
```

The frontend and API are separate services so they can scale and release
independently. The frontend image receives the exact API HTTPS origin at build
time. The API accepts browser requests only from the deployed frontend origin.
No wildcard CORS policy, database, secret or writable runtime volume is used.

## Provisioned resources

The deployment script creates or updates:

- the required Artifact Registry, Cloud Build and Cloud Run APIs;
- one regional Docker repository in Artifact Registry;
- one dedicated runtime service account without project roles;
- one public API service with zero minimum instances and one maximum instance;
- one public frontend service with zero minimum instances and one maximum instance;
- immutable images tagged with the current Git commit by default.

Cloud Run revisions resolve image tags to immutable digests. Artifact Registry
must exist before Cloud Build can publish an image. These constraints follow the
official [Cloud Run deployment](https://cloud.google.com/run/docs/deploying),
[Artifact Registry](https://cloud.google.com/artifact-registry/docs/repositories/create-repos)
and [Cloud Build](https://cloud.google.com/build/docs/build-push-docker-image)
workflows.

## Prerequisites

Do not run the deployment until all of these are true:

1. a GCP project exists and billing is enabled;
2. Google Cloud CLI is installed and current;
3. `gcloud auth login` has completed;
4. the active account can enable APIs, create Artifact Registry repositories,
   submit Cloud Build jobs, create service accounts and administer Cloud Run;
5. the Git working tree is clean and the repository quality gate passes.

Cloud Build's active build identity also needs permission to upload to the
same-project Artifact Registry repository. Organization policies may prohibit
public Cloud Run invocation; in that case, do not weaken policy—choose an
authenticated access design before deploying.

## Deployment command

From the project root:

```powershell
.\deployment\gcp\deploy.ps1 -ProjectId "YOUR_GCP_PROJECT_ID"
```

Optional parameters:

```powershell
.\deployment\gcp\deploy.ps1 `
  -ProjectId "YOUR_GCP_PROJECT_ID" `
  -Region "us-central1" `
  -Repository "retail-intelligence" `
  -ImageTag "v1.0.0"
```

The script waits for newly enabled Google APIs to become queryable and stops on
the first non-transient failed command. A successful run prints the two Cloud
Run URLs only after health and schema smoke checks pass.

## Security boundary

- Both services are public because this release has no identity module.
- The API permits only `GET`; CORS is narrowed to the exact web origin.
- The runtime identity receives no project-level role.
- Images contain the synthetic learning evidence already tracked by Git.
- No service-account key, token, `.env` file or credential belongs in Git.
- Production data, authentication and authorization require a separate design.

## Cost and cleanup

Both services use request-based scaling with zero minimum instances and one
maximum instance. CPU is throttled outside request processing and the optional
startup CPU boost is disabled. This sharply limits exposure but cannot
guarantee a zero invoice: Cloud Build, Artifact Registry storage, network
traffic, logging and Cloud Run requests may still incur charges after their
applicable allowances. Review current GCP pricing and budgets before running
the script.

To remove the two runtime services after a demonstration:

```powershell
gcloud run services delete retail-intelligence-web --region us-central1
gcloud run services delete retail-intelligence-api --region us-central1
```

Delete the Artifact Registry repository only if its stored release images are
no longer needed.
