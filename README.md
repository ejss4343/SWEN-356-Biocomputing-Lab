# Biocomputing Lab Simulator

An interactive pygame simulation exploring a landmark biocomputing study:
- **Cornell Organic Robotics Lab** — biohybrid robots controlled by fungal electrical impulses

---

## Setup & Running

**Requirements:** Python 3.8+

```bash
pip install -r requirements.txt
python lab_sim.py
```

> `requirements.txt` uses `pygame-ce` (Pygame Community Edition), a maintained fork of pygame.

---

## Simulations

### 1. Robot Simulation (10–15 min)

Models the Cornell experiment where a biohybrid robot's movement is driven by fungal mycelia electrical signals across three scenarios.

**Controls:**

| Key | Action |
|-----|--------|
| `1` | Natural Mode — robot moves from raw, noisy mycelia signals |
| `2` | UV Mode — toggle UV stimulation |
| `3` | Override Mode — you directly control the signal with arrow keys |
| `W A S D` / `← ↑ ↓ →` | influence (Mode 2) or control (Mode 3) movement |
| `ESC` | Return to menu |

**Goal:** Navigate the mushroom robot to the target under each mode.

---

## References

- [Biohybrid robots controlled by electrical impulses — in mushrooms (Cornell)](https://news.cornell.edu/stories/2024/08/biohybrid-robots-controlled-electrical-impulses-mushrooms)
