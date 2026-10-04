# Optional — Deploy to the Public Web with Render

> [!NOTE]
> This is an **optional extension** for after the main workshop. It makes your Grade Predictor accessible from any browser, anywhere in the world.

## What you need

- The CI pipeline from Exercise 3 must have completed successfully at least once, so the image exists on Docker Hub.
- A free [Render](https://render.com/) account.
- Your Docker Hub username (`DOCKERHUB_USERNAME`).

The image you pushed in CI is:

```
<your-dockerhub-username>/grade-predictor:latest
```

---

## Steps

### 1. Create a Render account

Sign up at [render.com](https://render.com/) — the free tier is enough for this workshop.

### 2. Create a new Web Service

1. In the [Render Dashboard](https://dashboard.render.com/), click **+ New → Web Service**.
2. Under **Source Code**, click **Existing Image**.
3. In the **Image URL** field, enter:

   ```
   <your-dockerhub-username>/grade-predictor:latest
   ```

   If the image is **public** on Docker Hub, no credentials are needed — skip to step 5.

### 3. Add credentials (private images only)

If your Docker Hub repository is private:

1. Click **Add credential**.
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | `Docker Hub` (any label) |
   | Registry | Docker Hub |
   | Username | Your Docker Hub username |
   | Personal Access Token | A token from [hub.docker.com/settings/security](https://hub.docker.com/settings/security) |

3. Click **Add**.

### 4. Verify and connect

Render will verify it can pull the image. Click **Connect** once it succeeds.

### 5. Configure the service

| Setting | Value |
|---|---|
| Name | `grade-predictor` (or anything you like) |
| Region | Closest to you |
| Instance type | **Free** |
| Port | `8000` |

Leave everything else as default.

### 6. Deploy

Click **Deploy Web Service**.

Render will pull your Docker image and start the container. The first deploy takes 1–2 minutes.

Once it is done, you will see a public URL like:

```
https://grade-predictor-xxxx.onrender.com
```

Click it — your app is live.

---

## Triggering future deploys

Render does **not** automatically redeploy when a new image is pushed to Docker Hub. To redeploy after a new CI run:

**Option A — Manual deploy (simplest):**

In the Render Dashboard, select your service and click **Manual Deploy → Deploy latest reference**.

**Option B — Deploy webhook (automated):**

1. Go to your service's **Settings** page on Render and copy the **Deploy Hook URL**.
2. Add a new step to the `docker` job in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml):

   ```yaml
   - name: Trigger Render deploy
     run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
   ```

3. Add `RENDER_DEPLOY_HOOK_URL` as a GitHub repository secret (the value is the URL you copied from Render).

   Now every successful CI push also redeploys your live service automatically.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `Image Pull Failed` | Check the image URL and credentials in Render's service Settings |
| `/bin/sh: [uvicorn,: not found` | The `CMD` in your Dockerfile is missing the closing `]` — see Exercise 2 |
| App loads but crashes | Check the Render logs tab for the Python traceback |
| Port not accessible | Make sure your service port is set to `8000` in Render's settings |

---

## Further reading

- [Render: Deploy a Prebuilt Docker Image](https://render.com/docs/deploying-an-image)
- [Render: Deploy Hooks](https://render.com/docs/deploy-hooks)
- [Docker Hub: Personal Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
