# Workflow of the Dashboard Manager

```mermaid
graph TD
    DM[Dashboard Management] -->|Manages| DLE[Dashboard Layouts Editor]
    DM -->|Manages| DIE[Dashboard Items Editor]
    DLE -->|Interacts with| DB[(Database)]
    DIE -->|Interacts with| DB
    DM -->|Uses| SE[Streamlit Elements]
    DM -->|Uses| S[Streamlit]
    DM -->|Utilizes| C[Components]
    C -->|Includes| U[Utils]
    C -->|Includes| DS[Datastore]
    U -->|Assists in managing| DLE
    U -->|Assists in managing| DIE
    DS -->|Stores| DLE
    DS -->|Stores| DIE
```

# Logic of Dashboard build

```mermaid
graph TD
    E[Elements Module] -->|Contains| D[Dashboard Module]
    D -->|Defines| L[Layout]
    L -->|Includes| I1[Item 1: Draggable and Resizable]
    L -->|Includes| I2[Item 2: Not Draggable]
    L -->|Includes| I3[Item 3: Not Resizable]

    D -->|Utilizes| G[Grid]
    G -->|Contains| P1[Paper 1]
    G -->|Contains| P2[Paper 2]
    G -->|Contains| P3[Paper 3]

    G -->|Optional| LC[Layout Change Handler]
    LC -->|Updates| L
```

### process and components of the dashboard when it is needed, created, or updated

```mermaid
graph TD
    A[Start] --> B[Identify Need for Dashboard]
    B --> C[Define Dashboard Layout]
    C -->|Layout Includes| I1[Item 1: Draggable and Resizable]
    C -->|Layout Includes| I2[Item 2: Not Draggable]
    C -->|Layout Includes| I3[Item 3: Not Resizable]

    C --> D[Implement Grid Structure]
    D --> E[Place Items in Grid]
    E -->|Item 1| P1[Paper 1]
    E -->|Item 2| P2[Paper 2]
    E -->|Item 3| P3[Paper 3]

    E --> F[Optional: Layout Change Handler]
    F -->|Update Layout| C

    E --> G[Dashboard Creation Complete]
    G --> H[Monitor and Update as Needed]
    H -->|Update Required| C
    H -->|No Update Required| I[Dashboard Operational]


```

# Dashboard testing setup

```mermaid
graph TD
    A[Start] -->|User selects a dashboard| B[Dashboard Selector]
    B --> C[Load Dashboard Function]
    C -->|Retrieve Layout| D[Load Existing Layout]
    D --> E[Initialize Streamlit Elements]
    E --> F[Build Default Layout]
    F -->|Define Items| G[Dashboard Item]
    G --> H[Create Dashboard Grid]
    H -->|Attach Papers| I[Paper Components]
    H -->|Optional| J[Handle Layout Change]
    J -->|Update Layout| F

    subgraph Dashboard Selector
    B
    end

    subgraph Load Dashboard Function
    C --> D
    end

    subgraph Dashboard Grid
    H
    end

```

This diagram illustrates the following process:

1. **Start**: The process begins with the user selecting a dashboard.
2. **Dashboard Selector**: The user's selection triggers the `load_dashboard` function.
3. **Load Dashboard Function**: This function loads the existing layout for the selected dashboard.
4. **Initialize Streamlit Elements**: Streamlit Elements are initialized for dashboard creation.
5. **Build Default Layout**: A default layout is built with specified dashboard items.
6. **Dashboard Item**: Individual items are defined for the dashboard.
7. **Create Dashboard Grid**: A grid layout is created to place the dashboard items.
8. **Paper Components**: Paper components are attached to the grid.
9. **Handle Layout Change (Optional)**: Optionally, any layout changes made by the user can be handled and used to update the layout.
