# GachaMC

> Python GUI tool for modeling, simulating and optimizing currency flows.

An important part of video game design is the modeling and balancing of currency flows. Especially gacha games are characterized by an abundance of in-game currencies and complex interactions between them involving conversion rates, randomized rewards and mini games. GachaMC allows users to model these interactions as a currency flow graph such that currency generation and conversion can be simulated and later optimized.

![screenshot](https://user-images.githubusercontent.com/36499405/218109397-0f850833-6102-4ec4-8833-c5e546bff38a.PNG)


## Installation

To install the executable for Windows, Linux and MacOS please check out the releases section of this repository.

In order to install from terminal use
```
$ pip install -r requirements.txt
```
and run with
```
$ python3 app.py
```


## Usage

### Sources and Currencies

Sources and currencies can be added by using the buttons `Add Source` and `Add Currency` on the left.

**Currencies** represent tangible quantities of interest in an economy. They may represent actual money, resources such as iron or gold or time. Currencies are represented by circles and a target value can be configured by clicking on them. The target value is what the economy is working towards and typically means that the player enters a new game loop by unlocking new mechanics or areas. If target values are set for multiple currencies the simulation will optimize to reach all target values as soon as possible.

**Sources** represent producers of currencies. They connect pools of currencies together and thus form the edges of the currency graph. Each source can have inputs and outputs that are configured by clicking on the source and pressing the buttons `Add Input` or `Add Output` on the right hand side respectively. Additionally, a time requirement can be set by changing the time step number. If fully configured the source is handled as consuming one set of inputs and producing one set of outputs in the given number of time steps.

### Saving and Loading

The currency graph is saved and loaded in YAML format. In order to save press the `Save Graph` button on the left and select a location. In order to load the graph again press the `Load Graph` button and select the respective YAML file.

### Simulating the Currency Flow

Once the flow graph is correctly set up it can be simulated by pressing the play button in the bottom. This will compute the nearly optimal currency production rates and then simulate how long it takes to reach all configured target values for all currencies. The simulation cannot run if there is not at least one source, one currency and one connection between them.

After the simulation is run a second window will open with the results. This shows the status of the optimization as well as the simulated time it took to reach the target values of all currencies and the maximum throughput time given that the necessary input for all sources is already present in order for them to start producing. The results window shows the flow graph with an additional node for the target values to flow to and a plot of the available currency at each point in the simulation. Individual currencies can be selected with the drop down menu.


## How it Works

The simulation requires that each source knows the optimal production rate in order to arrive at the target currency values as quickly as possible. This optimization problem is a generalized maximum flow problem on a directed hypergraph and can be solved using linear programming. The simulation itself simply checks if the necessary inputs are already available for all sources in each time step and adds and subtracts the currencies if applicable.

### Theory

Let the target value for each currency $c \in \mathcal{C}$ be denoted by $x_c \in \mathbb{R}^+$ and the processing rate for each source $s \in \mathcal{S}$ by $f_s \in \mathbb{R}+$. Additionally each source has a minimum number of time steps $t_s \in \mathbb{R}^+$ required to perform the conversion, such that the rate is limited by $0 \leq f_s \leq \frac{1}{t_s}$.

To introduce a target for maximization a drain is added that shall be denoted by $d$. All currencies with positive target value are considered to be connected to the drain such that the only function to be maximized is the processing rate of the drain itself.

Each source $s$ represents a hyperedge connecting multiple input currencies to multiple output currencies and thus the linear constraints arise from the fact that the sum of outgoing currency cannot be larger than the sum of ingoing currency. For each currency $c$ the set of outgoing and incoming hyperedges is denoted by $\delta^-(c)$ and $\delta^+(c)$ respectively. Furthermore, connections are weighted with outgoing connections going from currency to source having weights $\eta_{cs}$ and incoming connections having weights $\gamma_{sc}$. These weights can be arranged into outgoing and incoming incidence matrices $\text{H}$ and $\Gamma$.

All together this yields the optimization problem over $d$ and $f_s$
$$\max d$$
$$\sum_{s \in \delta^-(c)} \gamma_{sc} f_s - \sum_{s \in \delta^+(c)} \eta_{cs} f_s - y_c d \geq 0 \enspace \forall c \in \mathcal{C}$$
$$0 \leq f_s \leq \frac{1}{t_s} \enspace \forall s \in \mathcal{S}$$

### Implementation

The constraints of the linear program can be computed directly from the model graph and it is then solved using `scipy.optimize.linprog`.

Since the solution is oftentimes not unique the secondary objective $-\sum_{s \in \mathcal{S}} f_s$ is added to yield the solution where the least currency is produced in total without prolonging the time it takes to reach the target value.


## Credits

- The tool mainly uses *PySide2* for its graphical user interface
- Icons are from [Font Awesome](https://fontawesome.com/icons)
- Logo was generated with [LOGO.com](https://logo.com/)

