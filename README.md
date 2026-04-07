# Biocomputing Lab Simulator

An interactive pygame simulation exploring two landmark biocomputing studies:
- **Cornell Organic Robotics Lab** — biohybrid robots controlled by fungal electrical impulses
- **Ohio State University** — mushroom-based organic memristors

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
| `2` | UV Mode — UV light biases the signal in one direction |
| `3` | Override Mode — you directly control the signal with arrow keys |
| `U` | Toggle UV stimulation (Mode 2 only) |
| `←` / `→` | Steer robot (Mode 3 only) |
| `ESC` | Return to menu |

**Goal:** Navigate the robot (green square) to the red target under each mode.

**Worksheet Questions:**

1. Describe the signal pattern in Natural Mode.
   - The signal is noisy and stochastic, fluctuating between positive and negative values with no consistent direction. It resembles a random walk, where movement emerges from unpredictable spikes rather than deliberate control.
   - *Key: Biological systems often produce structured randomness, not deterministic outputs.*

2. What does the signal graph look like in each mode?
   - Natural Mode: Irregular spikes centered around zero with no clear trend (high variability).
   - UV Mode: The graph becomes biased in one direction (e.g., more positive values), showing that external stimuli shift the distribution of signals.
   - Override Mode: The graph becomes highly structured and predictable, often showing flat or step-like patterns depending on user input.

3. Can you predict behavior from the graph?
   - In Natural Mode, prediction is difficult due to randomness.
   - In UV Mode, behavior becomes partially predictable because of directional bias.
   - In Override Mode, behavior is fully predictable, since the signal is directly controlled.
   - *Key: Predictability increases as control shifts from biological → hybrid → human-driven.*

4. How does UV stimulation change the signal?
   - UV stimulation biases the signal, increasing the likelihood of movement in a specific direction. Instead of purely random fluctuations, the signal becomes skewed, demonstrating responsiveness to environmental input.
   - *Key: This models how biological organisms react to external stimuli by altering internal electrical activity.*

5. Which mode is hardest? Which mode gives you the most control? Why?
   - Hardest: Natural Mode — movement is driven entirely by random signals with no external influence.
   - Most control: Override Mode — the user directly determines the signal, eliminating randomness.
   - Middle ground: UV Mode — partial control via environmental influence, but still some randomness.
   - *Key: This demonstrates a spectrum from fully autonomous biological systems → hybrid systems → fully controlled systems.*

6. What real-world systems behave like this?
   - Neural systems (brain signals influencing behavior)
   - Brain-computer interfaces (BCIs)
   - Autonomous robots with sensor input
   - Cyber-physical systems
   - Reinforcement learning agents with noisy environments
   - *Key: Many real systems operate under uncertainty + partial control, not perfect determinism.*

---

### 2. Memristor Simulation (10–15 min)

Models the OSU experiment where mushroom tissue acts as RAM, switching between electrical states with frequency-dependent accuracy.

**Controls:**

| Key | Action |
|-----|--------|
| `↑` / `↓` | Increase / decrease voltage |
| `←` / `→` | Decrease / increase signal frequency |
| `M` | Add another mushroom to the circuit |
| `ESC` | Return to menu |

**Goal:** Reach frequency ≥ 5 while keeping accuracy above 0.8.

**Worksheet Questions:**

1. What happens to accuracy as frequency increases?
   - Accuracy decreases as frequency increases, especially at higher values. This reflects the system's inability to reliably process signals at high speeds.
   - *Key: There is a performance limit beyond which the system becomes unstable or error-prone.*

2. How do additional mushrooms affect performance?
   - Adding more mushrooms improves accuracy, but with diminishing returns. Each additional unit contributes less improvement than the previous one.
   - *Key: This models parallelism and redundancy in biological systems.*

3. What tradeoff exists between speed and reliability?
   - Higher frequency (speed) → lower accuracy; lower frequency → higher accuracy.
   - *Key: Students should recognize this from networking (latency vs. throughput), distributed systems, and hardware design.*

4. How is this similar to neural systems?
   - Neurons have firing rate limits; high activity introduces noise and errors; reliability improves with redundancy (more neurons/connections); systems rely on distributed processing, not single perfect units.
   - *Key: The system behaves like a simplified neural network where memory is stateful, computation is distributed, and performance is probabilistic.*

---

## References

- [Biohybrid robots controlled by electrical impulses — in mushrooms (Cornell)](https://news.cornell.edu/stories/2024/08/biohybrid-robots-controlled-electrical-impulses-mushrooms)
- [Powered by mushrooms, living computers are on the rise (OSU)](https://news.osu.edu/powered-by-mushrooms-living-computers-are-on-the-rise/)
