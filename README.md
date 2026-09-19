[![Runpod](https://api.runpod.io/badge/ZeroClue/qwen-img-2512)](https://console.runpod.io/hub/ZeroClue/qwen-img-2512) [![Sign Up](https://img.shields.io/badge/RunPod-Sign%20Up-blue)](https://runpod.io?ref=lnnwdl3q)

# Qwen Image 2512 Generation

## Catline production contract

This fork's production path requires a pre-seeded RunPod Network Volume. Container startup validates
the pinned `models.json` manifest and its full-verification marker; it never downloads weights during
a cold start. Run `python /opt/catline/seed_models.py` from a temporary Pod to seed and SHA-256 verify
the volume.

Catline jobs generate exactly one `1080x1920` lossless WebP and upload it directly to the supplied
one-object R2 presigned PUT URL. The worker returns only `asset` metadata and timings—never base64,
signed URLs or permanent storage credentials. `output` is required for production jobs.

🚀 **Ultra-fast AI image generation in 4 or 8 steps** - Generate high-quality 1328×1328 images using the latest Qwen-Image-2512 model with Lightning LoRA optimization.

## 🎯 **Maximum Resolution: 4K Ultra HD**
- **4K Quality**: Up to 4096×4096 pixels (17 megapixels)
- **Flexible Resolutions**: Support from 512×512 up to 4K Ultra HD (4096×4096)
- **Production Ready**: High-resolution output for professional use

## ⚡ Key Features

- **Lightning Generation**: 4-step (fastest) or 8-step (balanced) Lightning LoRA — 6-12x faster than 50-step base model
- **Latest Model**: Qwen-Image-2512 — newest generation with improved quality
- **Triple Mode**: 4-step Lightning (fastest), 8-step Lightning (balanced), or 50-step full quality via `steps` parameter
- **Cost Efficient**: 80-90% reduction in generation costs vs standard models
- **Qwen Vision-Language**: Advanced Chinese/English text-to-image with excellent text rendering
- **Production Ready**: Optimized for RunPod Hub deployment

## 🎯 Performance Metrics

| Metric | Value | Comparison |
|--------|-------|------------|
| Generation Time (4-step) | 1-3 seconds | 10-12x faster than standard models |
| Generation Time (8-step) | 3-5 seconds | 6-8x faster than standard models |
| Generation Time (50-step) | 10-20 seconds | Full quality mode |
| Resolution | 1328×1328 pixels (default) | Up to 4096×4096 (4K) supported |
| Memory Usage | ~16GB GPU | Efficient resource utilization |
| Steps | Any positive integer | Auto-selects LoRA: <=4=4-step, 5-8=8-step, >8=base |

## 🏗️ Architecture

### Model Components
- **Base Model**: Qwen Image 2512 (diffusion model, fp8)
- **Text Encoder**: Qwen 2.5 VL 7B (multilingual understanding)
- **VAE**: Qwen Image VAE (efficient encoding/decoding)
- **LoRA**: Qwen-Image-Lightning-4steps-V1.0 + Qwen-Image-Lightning-8steps-V1.0 (speed optimization, auto-selected by steps)

### Pipeline Flow
```
Text Prompt → Qwen 2.5 VL Encoder → Qwen Image 2512 + Lightning LoRA → Sampling (4/8/N steps) → VAE Decode → Output Image
```

## 🚀 Quick Start

### RunPod Serverless (Recommended)
Deploy as a serverless API endpoint for scalable, pay-per-use generation:

1. Visit the Qwen Image 2512 listing on RunPod Hub
2. Select GPU (A10G minimum, A40/A100 recommended)
3. Launch and start generating images instantly

```bash
# Clone the repository
git clone https://github.com/ZeroClue/qwen-img-2512.git
cd qwen-img-2512
```

### 🎁 Get Free Credits

**Sign up with our referral link** to get a credit bonus between $5-$500:
- **[Create Free RunPod Account](https://runpod.io?ref=lnnwdl3q)**
- Bonus credits are automatically applied to your account

## 📡 API Usage

### Simplified Prompt API (Recommended)
```python
import requests
import json
import base64

url = "https://api.runpod.ai/v2/{endpoint_id}/runsync"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

payload = {
    "input": {
        "prompt": "A cat sitting on a windowsill, warm afternoon sunlight, photorealistic",
        "seed": 42,
        "width": 1328,
        "height": 1328,
        "steps": 4,
        "negative_prompt": "",
        "batch_size": 1
    }
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

# Decode base64 image
image_data = base64.b64decode(result["images"][0]["data"])
with open("output.png", "wb") as f:
    f.write(image_data)
```

### Simplified API Parameters

| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `prompt` | ✅ | — | Text description of the image |
| `seed` | ❌ | random | Reproducibility seed |
| `width` | ❌ | 1328 | Image width (up to 4096) |
| `height` | ❌ | 1328 | Image height (up to 4096) |
| `steps` | ❌ | 4 | Inference steps (any positive int). Auto-selects LoRA: ≤4→4-step, 5-8→8-step, >8→base |
| `negative_prompt` | ❌ | "" | What to avoid in generation |
| `batch_size` | ❌ | 1 | Number of images per request |
| `lora` | ❌ | auto | Override LoRA: `"4step"`, `"8step"`, `"none"`. Auto-detect from steps: ≤4→4-step, 5-8→8-step, >8→base |
| `cfg` | ❌ | auto | CFG scale (auto: 1.0 for Lightning, 4.0 for base) |
| `shift` | ❌ | 3.1 | ModelSamplingAuraFlow shift — increase if blurry/dark, decrease for more detail |
| `sampler` | ❌ | `"euler"` | KSampler sampler name (e.g. `euler`, `res_multistep`) |
| `scheduler` | ❌ | `"simple"` | KSampler scheduler name |

### Raw Workflow Mode
For advanced users, pass a complete ComfyUI API-format workflow:
```python
payload = {
    "input": {
        "workflow": { ... }  # Full ComfyUI node graph
    }
}
```

## 💰 Pricing & Deployment Costs

### RunPod Serverless (Most Cost-Effective)
- **Per-Generation (4-step)**: ~$0.002-$0.004 per image
- **Per-Generation (50-step)**: ~$0.01-$0.02 per image
- **Pay-per-second**: Only pay for actual generation time
- **Auto-scaling**: Zero cost when not in use

### Cost Comparison (per image)
| Steps | Time/Gen | Cost/Gen | Monthly (1000 imgs) |
|-------|----------|----------|---------------------|
| **4 (Lightning)** | 1-3s | $0.003 | $3.00 |
| **8 (Lightning)** | 3-5s | $0.006 | $6.00 |
| **50 (Full)** | 10-20s | $0.015 | $15.00 |

## 🔧 Configuration

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `COMFY_ORG_API_KEY` | Comfy.org API key for API Nodes |
| `BUCKET_ENDPOINT_URL` | S3 endpoint for image uploads |
| `HF_TOKEN` | HuggingFace token for faster model downloads |
| `COMFY_LOG_LEVEL` | ComfyUI verbosity (default: DEBUG) |
| `REFRESH_WORKER` | Restart worker after each job |

### Resource Requirements
- **GPU**: A10G (minimum) / A40 (recommended) / A100 / RTX 5090 (optimal)
- **GPU Memory**: 16GB+ required
- **Container Disk**: 50GB recommended (models download at runtime, ~32GB total)

## 📁 File Structure

```
qwen_img_2512/
├── .runpod/               # RunPod Hub configuration
│   ├── Dockerfile         # Hub build configuration
│   └── hub.json           # Hub metadata and specs
├── src/
│   ├── start.sh           # Container entrypoint
│   ├── check-models.sh    # Model download/validation
│   └── extra_model_paths.yaml  # Network volume mapping
├── scripts/
│   ├── comfy-node-install.sh
│   └── comfy-manager-set-mode.sh
├── handler.py             # RunPod serverless handler
├── Dockerfile             # Container build configuration
├── docker-bake.hcl        # Docker Bake build targets
├── example-request.json   # Simplified API example
├── simplified-request.json # Minimal prompt example
├── test_input.json        # Test workflow
└── requirements.txt       # Python dependencies
```

## 🆚 Comparison with Original Qwen Image 8-Step

| Feature | Qwen Image (8-step) | Qwen Image 2512 |
|---------|---------------------|------------------|
| **Model** | Original Qwen Image | Qwen Image 2512 (newer) |
| **Lightning Steps** | 8 | 4 or 8 (flexible) |
| **Full Steps** | N/A | 50 (or any positive integer) |
| **Quality** | High | Improved |
| **Text Rendering** | Good | Better |

## 📄 License

- **Models**: Apache-2.0 compatible licenses
- **Commercial Use**: ✅ Allowed with attribution

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/ZeroClue/qwen-img-2512/issues)
- **Community**: Join the RunPod Discord for community support
