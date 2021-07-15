# Incremental Victor

This was an experiment of mine, where I created a dynamic version of Victor that kept up-to-date with the position as it changed.

In the original paper, Allis noted that creating the NodeGraph was the most expensive part of evaluating a position. I thought that I might be able to save some computation time by saving connections between problems<->solutions and solutions<->solutions.

However, this failed for two reasons:
1. The graph changes a lot with each position.
2. We only use Victor to evaluate leaf nodes and there are lots of positions where we don't evaluate it at all.
