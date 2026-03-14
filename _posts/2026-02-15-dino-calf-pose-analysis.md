---
layout: post
title: "DINO Features for Calf Pose Classification"
date: 2026-02-15
tags: [research, computer-vision, deep-learning]
excerpt: "Using self-supervised DINO features for posture recognition in overhead video of dairy calves."
---

In the Sun Lab, we're building computer vision pipelines to help veterinary researchers analyze dairy calf behavior at scale. One challenge: classifying calf posture (standing, lying, etc.) from overhead video without massive labeled datasets.

## Why DINO?

DINO (self-distillation with no labels) produces rich visual features from unlabeled images. We extract features from a pretrained DINO model and train lightweight classifiers on top—no need to fine-tune the whole backbone. This works well when labeled data is limited.

## Pipeline Overview

1. **Frame extraction** — Sample frames from overhead video
2. **DINO feature extraction** — Run each crop through DINO, take the [CLS] token or patch embeddings
3. **Classifier** — Simple MLP or linear probe on the feature vectors
4. **Evaluation** — Cross-validate on our self-annotated calf dataset

## Early Results

We're seeing solid accuracy on binary and multi-class posture tasks. The main bottleneck is annotation quality—veterinary researchers need clear guidelines for ambiguous poses. Next steps: improve the annotation workflow and test VLMs for zero-shot pose recognition.
