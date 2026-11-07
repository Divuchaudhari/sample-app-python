\# Enterprise CI/CD + DevSecOps Platform



A reusable CI/CD and DevSecOps platform: standard pipelines for testing,

security scanning, container scanning, multi-environment deployment,

progressive delivery with automatic rollback, and DORA metrics.



The platform is split into two repositories:



\- \*\*platform-pipelines\*\*: the shared, reusable workflows (the "company standard")

\- \*\*sample-app-python\*\* (this repo): a sample Flask app that calls them



\## Architecture



```mermaid

flowchart LR

&#x20; Dev\["Developer"] --> PR\["Pull request"]

&#x20; PR --> CI\["ci: lint + unit tests"]

&#x20; PR --> SEC\["security: Gitleaks, Semgrep, pip-audit"]

&#x20; PR --> CON\["container: build + Trivy scan"]

&#x20; CI --> Merge\["Merge to main"]

&#x20; SEC --> Merge

&#x20; CON --> Merge

&#x20; Merge --> Build\["Build image once"]

&#x20; Build --> DEV\["Deploy dev + smoke test"]

&#x20; DEV --> STG\["Deploy staging + smoke test"]

&#x20; STG --> APPROVAL{"Manual approval"}

&#x20; APPROVAL --> PROD\["Deploy production"]

```



\## Progressive delivery and automatic rollback



```mermaid

flowchart LR

&#x20; A\["New release"] --> B\["Canary: 20 percent of pods"]

&#x20; B --> C{"Prometheus: error rate under 5 percent?"}

&#x20; C -- yes --> D\["50 percent, then 100 percent"]

&#x20; C -- no --> E\["Automatic rollback"]

```



\## What is implemented



| Area | What I built |

|---|---|

| Reusable pipelines | company-ci, company-security, company-container and company-deployment workflows in platform-pipelines. The app repo calls them in a few lines. |

| Security gates | Gitleaks (secrets), Semgrep (SAST), pip-audit (dependencies), Trivy (container image). All are required checks. |

| Branch protection | A GitHub ruleset on main requires a pull request and all 5 status checks. |

| Deployment | Build the image once, then promote the same image through dev, staging and production using GitHub Environments. Production needs manual approval. |

| Packaging | Helm chart with per-environment values (1, 2 and 3 replicas) and health probes. |

| Progressive delivery | Argo Rollouts canary (20%, 50%, 100%). |

| Automatic rollback | An AnalysisTemplate queries Prometheus for the canary's 5xx error rate and aborts the release if it is above 5%. A bad release was rolled back with no human action. |

| DORA metrics | A script and a scheduled workflow report deployment frequency, lead time, change failure rate and mean time to recovery. |



\## Honest scope



\- The pipeline deploys to a temporary kind (Kubernetes in Docker) cluster

&#x20; inside the GitHub runner. The same Helm commands work on a real cluster such as EKS.

\- Canary analysis and rollback were demonstrated on a local kind cluster with

&#x20; Prometheus and Argo Rollouts.

\- Built with one sample app. The shared workflows are designed to be called by many repositories.

\- A first image was pushed to Amazon ECR manually. Automating the push with

&#x20; GitHub OIDC is the planned next step.



\## Tools



GitHub Actions, Docker, Kubernetes (kind), Helm, Argo Rollouts, Prometheus,

Gitleaks, Semgrep, pip-audit, Trivy, Amazon ECR.

