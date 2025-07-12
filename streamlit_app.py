import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
import matplotlib.patches as patches

# --- Existing SeaSlug and EggMass Classes ---

class SeaSlug:
    """
    Represents a sea slug with specific reproductive characteristics.
    """
    def __init__(self, species, egg_count_range, egg_mass_shape, coiling_direction,
                 hatching_time_range, larval_type, is_toxic, preferred_substrate):
        self.species = species
        self.egg_count_range = egg_count_range  # (min, max) eggs
        self.egg_mass_shape = egg_mass_shape    # e.g., "spiral ribbon", "globular jelly mass", "flat sheet"
        self.coiling_direction = coiling_direction # e.g., "anticlockwise", "clockwise", "pseudodextral", "N/A"
        self.hatching_time_range = hatching_time_range # (min_days, max_days)
        self.larval_type = larval_type          # "planktotrophic veliger" or "lecithotrophic juvenile"
        self.is_toxic = is_toxic                # Boolean
        self.preferred_substrate = preferred_substrate # e.g., "rocks", "seaweed", "sediment"

    def mate(self, other_slug):
        """
        Simulates mating between two hermaphroditic sea slugs.
        Both slugs can become fertilized and lay eggs.
        """
        st.write(f"The {self.species} and {other_slug.species} are engaging in courtship and mating. Both are hermaphroditic and can lay eggs. [2, 3, 4]")
        return True

    def lay_eggs(self, substrate, temperature_celsius, water_flow_rate):
        """
        Simulates the process of a sea slug laying an egg mass.
        The process involves internal fertilization, secretion of gelatinous matrix,
        and physical shaping by the slug.
        """
        if substrate not in self.preferred_substrate:
            st.warning(f"Warning: {self.species} prefers {self.preferred_substrate} but is laying on {substrate}. This might affect egg mass stability. [5, 6]")

        num_eggs = random.randint(self.egg_count_range[0], self.egg_count_range[1])
        
        # Simulate the physical shaping of the egg mass
        st.write(f"The {self.species} begins extruding a continuous stream of fertilized eggs and gelatinous matrix from its genital aperture. [7, 8, 9]")
        st.write(f"Using its muscular foot and mantle edge, the slug actively manipulates and presses the material against the substrate, sculpting it into a **{self.egg_mass_shape}** with a **{self.coiling_direction}** coiling direction. [6, 10]")
        
        # Determine hatching time, influenced by temperature
        base_hatching_days = random.randint(self.hatching_time_range[0], self.hatching_time_range[1])
        
        # Temperature effect: warmer water generally accelerates development
        # Simplified model: -1 day for every 2 degrees above 20C, +1 day for every 2 degrees below 20C
        temperature_adjustment = (temperature_celsius - 20) // 2
        adjusted_hatching_days = max(5, base_hatching_days - temperature_adjustment) # Minimum 5 days [11, 12]

        egg_mass = EggMass(
            species=self.species,
            num_eggs=num_eggs,
            shape=self.egg_mass_shape,
            coiling_direction=self.coiling_direction,
            hatching_day=adjusted_hatching_days,
            larval_type=self.larval_type,
            is_toxic=self.is_toxic,
            substrate=substrate
        )
        st.success(f"A new egg mass of **{num_eggs:,}** eggs has been laid by the **{self.species}** on the **{substrate}**. It is a **{egg_mass.shape}** and will hatch in approximately **{egg_mass.hatching_day}** days (adjusted for {temperature_celsius}°C). [5, 13]")
        if egg_mass.is_toxic:
            st.info(f"This egg mass incorporates defensive toxins from the parent, deterring predators. [11, 12, 14, 15]")
        return egg_mass

class EggMass:
    """
    Represents a sea slug egg mass and simulates its development.
    """
    def __init__(self, species, num_eggs, shape, coiling_direction, hatching_day, larval_type, is_toxic, substrate):
        self.species = species
        self.num_eggs = num_eggs
        self.shape = shape
        self.coiling_direction = coiling_direction
        self.hatching_day = hatching_day
        self.larval_type = larval_type
        self.is_toxic = is_toxic
        self.substrate = substrate
        self.current_day = 0
        self.hatched = False
        self.survival_rate = 1.0 # Initial survival rate

    def simulate_development(self, current_day, temperature_celsius, water_flow_rate):
        """
        Simulates the daily development of the egg mass, considering environmental factors.
        """
        self.current_day = current_day
        st.markdown(f"### Day {self.current_day}")
        st.write(f"The **{self.species}** egg mass ({self.shape}, {self.num_eggs:,} eggs) on {self.substrate} is developing.")

        # Oxygen diffusion impact (simplified) [16, 17, 18, 19, 20, 21, 22]
        # Larger/denser masses in low flow or high temperature can experience hypoxia.
        oxygen_stress_factor = 0
        if self.num_eggs > 100000 and water_flow_rate < 0.5: # Arbitrary threshold for "large/dense" and "low flow"
            oxygen_stress_factor += 0.1
        if temperature_celsius > 25: # High temperature increases metabolic demand
            oxygen_stress_factor += 0.05
        
        if oxygen_stress_factor > 0:
            self.survival_rate -= (oxygen_stress_factor * 0.1) # Small daily reduction
            self.survival_rate = max(0, self.survival_rate)
            st.warning(f"Oxygen diffusion is a challenge due to environmental conditions (temp: {temperature_celsius}°C, flow: {water_flow_rate}). Current survival rate: {self.survival_rate:.2f}. [16, 17, 18, 19, 23, 20, 21, 22]")

        if self.current_day >= self.hatching_day and not self.hatched:
            num_surviving_eggs = int(self.num_eggs * self.survival_rate)
            st.success(f"The egg mass has reached its hatching day! Approximately **{num_surviving_eggs:,}** embryos are hatching. [5, 12]")
            if self.larval_type == "planktotrophic veliger":
                st.write(f"They are hatching as free-swimming, microscopic **veliger larvae**, entering the plankton for dispersal. Unfortunately, only a few of these will likely survive to adulthood. [5, 9]")
            else: # lecithotrophic juvenile
                st.write(f"They are hatching as small, crawling **juveniles**, resembling miniature adults. This direct development offers higher survival rates for fewer offspring. [5, 12]")
            self.hatched = True
        elif self.current_day < self.hatching_day:
            st.write(f"Embryos are developing within the gelatinous matrix. Hatching expected in {self.hatching_day - self.current_day} days.")
            # Simulate embryonic stages (simplified)
            if self.current_day == 1:
                st.write("Initial cleavage and gastrulation are underway. [8, 24, 25]")
            elif self.current_day == self.hatching_day // 2:
                st.write("Embryos are progressing to the trochophore stage, developing cilia and beginning to rotate within their capsules. [8, 9, 18]")
            elif self.current_day == self.hatching_day - 2:
                st.write("Embryos are in the late veliger stage, developing prominent cilia and rotating vigorously. [9, 18]")
        else:
            st.info("The egg mass has already hatched.")

# --- Visualization Class ---

class EggLayingVisualizer:
    """
    Creates bird's-eye view visualization of egg laying patterns being formed progressively.
    """
    
    def __init__(self, sea_slug, substrate, temperature, flow_rate):
        self.sea_slug = sea_slug
        self.substrate = substrate
        self.temperature = temperature
        self.flow_rate = flow_rate
        self.current_step = 0
        self.total_steps = 100  # More steps for smoother pattern progression
        self.center_x, self.center_y = 5, 5
        self.egg_positions = []  # Track all laid eggs
        self.slug_positions = []  # Track slug movement
        
    def get_step_info(self, step):
        """Returns title and description for each step."""
        progress = step / self.total_steps
        if progress < 0.1:
            return ("Positioning", "Sea slug finds optimal laying position")
        elif progress < 0.2:
            return ("First Contact", "Beginning to lay eggs and form matrix")
        elif progress < 0.9:
            return ("Pattern Formation", f"Actively creating {self.sea_slug.egg_mass_shape} pattern")
        else:
            return ("Completion", "Egg mass pattern complete")
    
    def create_visualization(self, step):
        """Creates a bird's-eye view of the progressive egg laying pattern."""
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        
        # Set ocean-like background
        ax.set_facecolor('#004466')
        
        # Draw substrate from bird's eye view
        self._draw_substrate_overhead(ax)
        
        # Calculate current pattern progress
        progress = step / self.total_steps
        
        # Generate and draw the egg laying pattern
        if "spiral" in self.sea_slug.egg_mass_shape.lower():
            self._draw_spiral_pattern(ax, progress)
        elif "ribbon" in self.sea_slug.egg_mass_shape.lower():
            self._draw_ribbon_pattern(ax, progress)
        elif "cluster" in self.sea_slug.egg_mass_shape.lower():
            self._draw_cluster_pattern(ax, progress)
        else:
            self._draw_coil_pattern(ax, progress)
        
        # Draw sea slug at current position
        self._draw_slug_overhead(ax, progress)
        
        # Add grid and labels
        ax.grid(True, alpha=0.2, color='white')
        ax.set_title(f"Bird's Eye View: {self.get_step_info(step)[0]}", 
                    fontsize=14, fontweight='bold', color='white')
        ax.set_xlabel("Distance (cm)", fontsize=10, color='white')
        ax.set_ylabel("Distance (cm)", fontsize=10, color='white')
        
        # Add environment info
        self._add_environment_overlay(ax)
        
        return fig
    
    def _draw_substrate_overhead(self, ax):
        """Draw substrate from overhead view."""
        if self.substrate == "rock":
            # Rocky surface with texture
            rock = plt.Circle((self.center_x, self.center_y), 4, 
                            facecolor='#666666', edgecolor='#444444', linewidth=2, alpha=0.8)
            ax.add_patch(rock)
            # Add rock texture spots
            for i in range(15):
                x = self.center_x + random.uniform(-3, 3)
                y = self.center_y + random.uniform(-3, 3)
                if (x - self.center_x)**2 + (y - self.center_y)**2 <= 16:  # Within rock
                    spot = plt.Circle((x, y), random.uniform(0.1, 0.3), 
                                    color='#555555', alpha=0.6)
                    ax.add_patch(spot)
        elif self.substrate == "seaweed":
            # Seaweed fronds
            for i in range(8):
                angle = i * 45
                x = self.center_x + 2 * np.cos(np.radians(angle))
                y = self.center_y + 2 * np.sin(np.radians(angle))
                frond = plt.Circle((x, y), 0.8, color='#2d5016', alpha=0.7)
                ax.add_patch(frond)
        else:
            # Default substrate (sediment/coral)
            substrate = plt.Circle((self.center_x, self.center_y), 3.5, 
                                 facecolor='#8B7355', edgecolor='#654321', alpha=0.8)
            ax.add_patch(substrate)
    
    def _draw_spiral_pattern(self, ax, progress):
        """Draw progressive spiral egg laying pattern."""
        # Spiral parameters
        max_turns = 3 if "large" in self.sea_slug.egg_mass_shape else 2
        max_radius = 2.5
        
        # Calculate how much of spiral to show
        total_angle = max_turns * 2 * np.pi
        current_angle = total_angle * progress
        
        # Generate spiral points
        angles = np.linspace(0, current_angle, int(current_angle * 20))
        
        for i, angle in enumerate(angles):
            radius = (angle / total_angle) * max_radius
            x = self.center_x + radius * np.cos(angle)
            y = self.center_y + radius * np.sin(angle)
            
            # Egg mass thickness varies along spiral
            thickness = 0.15 + 0.1 * np.sin(angle * 2)
            
            # Color gradient from fresh (yellow) to older (orange)
            age_factor = i / len(angles) if len(angles) > 0 else 0
            color = plt.cm.YlOrRd(0.3 + 0.4 * age_factor)
            
            # Draw egg mass segment
            egg_mass = plt.Circle((x, y), thickness, color=color, alpha=0.8)
            ax.add_patch(egg_mass)
            
            # Add individual eggs within the mass
            if i % 5 == 0:  # Every 5th segment
                for j in range(3):
                    egg_x = x + random.uniform(-thickness/2, thickness/2)
                    egg_y = y + random.uniform(-thickness/2, thickness/2)
                    egg = plt.Circle((egg_x, egg_y), 0.03, color='white', alpha=0.9)
                    ax.add_patch(egg)
        
        # Current laying position (bright spot)
        if progress > 0 and len(angles) > 0:
            current_radius = (current_angle / total_angle) * max_radius
            curr_x = self.center_x + current_radius * np.cos(current_angle)
            curr_y = self.center_y + current_radius * np.sin(current_angle)
            current_spot = plt.Circle((curr_x, curr_y), 0.2, color='#FFD700', alpha=1.0)
            ax.add_patch(current_spot)
    
    def _draw_ribbon_pattern(self, ax, progress):
        """Draw progressive ribbon egg laying pattern."""
        # Ribbon parameters
        ribbon_length = 4
        waves = 2
        
        # Calculate current ribbon length
        current_length = ribbon_length * progress
        
        # Generate ribbon points
        t_values = np.linspace(0, current_length, int(current_length * 25))
        
        for i, t in enumerate(t_values):
            # Sinusoidal ribbon path
            x = self.center_x - 2 + t
            y = self.center_y + 0.5 * np.sin(waves * np.pi * t / ribbon_length)
            
            # Ribbon width
            width = 0.12 + 0.05 * np.sin(4 * np.pi * t / ribbon_length)
            
            # Color gradient
            age_factor = i / len(t_values) if len(t_values) > 0 else 0
            color = plt.cm.YlOrRd(0.2 + 0.5 * age_factor)
            
            # Draw ribbon segment
            ribbon_seg = plt.Circle((x, y), width, color=color, alpha=0.8)
            ax.add_patch(ribbon_seg)
            
            # Add eggs
            if i % 4 == 0:
                for j in range(2):
                    egg_x = x + random.uniform(-width, width)
                    egg_y = y + random.uniform(-width, width)
                    egg = plt.Circle((egg_x, egg_y), 0.025, color='white', alpha=0.9)
                    ax.add_patch(egg)
        
        # Current laying position
        if progress > 0 and len(t_values) > 0:
            current_t = current_length
            curr_x = self.center_x - 2 + current_t
            curr_y = self.center_y + 0.5 * np.sin(waves * np.pi * current_t / ribbon_length)
            current_spot = plt.Circle((curr_x, curr_y), 0.15, color='#FFD700', alpha=1.0)
            ax.add_patch(current_spot)
    
    def _draw_cluster_pattern(self, ax, progress):
        """Draw progressive cluster egg laying pattern."""
        max_clusters = 8
        current_clusters = int(max_clusters * progress)
        
        # Predefined cluster positions
        cluster_positions = []
        for i in range(max_clusters):
            angle = i * 2 * np.pi / max_clusters
            radius = 1.5 + 0.5 * (i % 2)  # Alternating radii
            x = self.center_x + radius * np.cos(angle)
            y = self.center_y + radius * np.sin(angle)
            cluster_positions.append((x, y))
        
        for i in range(current_clusters):
            x, y = cluster_positions[i]
            
            # Cluster size varies
            cluster_size = 0.2 + 0.1 * random.random()
            
            # Color based on order (older = more orange)
            age_factor = i / max_clusters
            color = plt.cm.YlOrRd(0.3 + 0.4 * age_factor)
            
            # Main cluster
            cluster = plt.Circle((x, y), cluster_size, color=color, alpha=0.8)
            ax.add_patch(cluster)
            
            # Individual eggs in cluster
            for j in range(5):
                egg_x = x + random.uniform(-cluster_size, cluster_size)
                egg_y = y + random.uniform(-cluster_size, cluster_size)
                egg = plt.Circle((egg_x, egg_y), 0.03, color='white', alpha=0.9)
                ax.add_patch(egg)
        
        # Show next cluster position if in progress
        if current_clusters < max_clusters:
            next_x, next_y = cluster_positions[current_clusters]
            next_spot = plt.Circle((next_x, next_y), 0.1, color='#FFD700', alpha=0.7)
            ax.add_patch(next_spot)
    
    def _draw_coil_pattern(self, ax, progress):
        """Draw progressive coil/tube pattern (for Aglajids)."""
        # Coil parameters
        coil_radius = 1.5
        coil_height = 0.3
        turns = 4
        
        # Current progress through coil
        current_turn = turns * progress
        
        # Generate coil points
        angles = np.linspace(0, current_turn * 2 * np.pi, int(current_turn * 30))
        
        for i, angle in enumerate(angles):
            # Coil position
            x = self.center_x + coil_radius * np.cos(angle)
            y = self.center_y + coil_radius * np.sin(angle)
            
            # Add vertical component (simulated in 2D)
            vertical_offset = coil_height * (angle / (2 * np.pi)) % coil_height
            x += vertical_offset * 0.1  # Slight offset to show coiling
            
            # Tube thickness
            thickness = 0.1
            
            # Color gradient
            age_factor = i / len(angles) if len(angles) > 0 else 0
            color = plt.cm.YlOrRd(0.3 + 0.4 * age_factor)
            
            # Draw tube segment
            tube_seg = plt.Circle((x, y), thickness, color=color, alpha=0.8)
            ax.add_patch(tube_seg)
            
            # Add eggs
            if i % 6 == 0:
                egg = plt.Circle((x, y), 0.02, color='white', alpha=0.9)
                ax.add_patch(egg)
        
        # Current laying position
        if progress > 0 and len(angles) > 0:
            current_angle = current_turn * 2 * np.pi
            curr_x = self.center_x + coil_radius * np.cos(current_angle)
            curr_y = self.center_y + coil_radius * np.sin(current_angle)
            current_spot = plt.Circle((curr_x, curr_y), 0.12, color='#FFD700', alpha=1.0)
            ax.add_patch(current_spot)
    
    def _draw_slug_overhead(self, ax, progress):
        """Draw sea slug from overhead view at current laying position."""
        if "spiral" in self.sea_slug.egg_mass_shape.lower():
            # Slug follows spiral path
            max_turns = 3 if "large" in self.sea_slug.egg_mass_shape else 2
            total_angle = max_turns * 2 * np.pi * progress
            radius = (total_angle / (max_turns * 2 * np.pi)) * 2.5
            slug_x = self.center_x + radius * np.cos(total_angle)
            slug_y = self.center_y + radius * np.sin(total_angle)
            slug_angle = total_angle + np.pi/2  # Perpendicular to spiral
            
        elif "ribbon" in self.sea_slug.egg_mass_shape.lower():
            # Slug follows ribbon path
            ribbon_length = 4 * progress
            slug_x = self.center_x - 2 + ribbon_length
            slug_y = self.center_y + 0.5 * np.sin(2 * np.pi * ribbon_length / 4)
            slug_angle = 0  # Facing forward along ribbon
            
        else:
            # Default positioning
            slug_x, slug_y = self.center_x, self.center_y
            slug_angle = 0
        
        # Draw slug body (elongated oval)
        slug_length, slug_width = 0.6, 0.3
        slug_body = Ellipse((slug_x, slug_y), slug_length, slug_width, 
                          angle=np.degrees(slug_angle), 
                          facecolor='orange', edgecolor='darkorange', alpha=0.9)
        ax.add_patch(slug_body)
        
        # Draw tentacles/rhinophores
        for offset in [-0.1, 0.1]:
            tentacle_x = slug_x + 0.2 * np.cos(slug_angle) 
            tentacle_y = slug_y + 0.2 * np.sin(slug_angle) + offset
            tentacle = plt.Circle((tentacle_x, tentacle_y), 0.05, color='red', alpha=0.8)
            ax.add_patch(tentacle)
    
    def _add_environment_overlay(self, ax):
        """Add environmental condition indicators."""
        # Temperature indicator (top-left) - using text instead of emoji
        temp_color = '#ff4444' if self.temperature > 25 else '#4444ff' if self.temperature < 15 else '#44ff44'
        ax.text(0.5, 9.5, f'TEMP: {self.temperature}°C', fontsize=12, color=temp_color, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Flow indicator (top-right) - using arrows instead of emoji
        flow_arrows = '→' * int(self.flow_rate * 5 + 1)
        ax.text(8.5, 9.5, f'FLOW: {flow_arrows}', fontsize=12, color='#00aaff',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        # Substrate indicator (bottom-left) - using text instead of emojis
        substrate_names = {
            'rock': 'ROCK', 
            'seaweed': 'SEAWEED', 
            'coral': 'CORAL',
            'sediment': 'SEDIMENT'
        }
        substrate_text = substrate_names.get(self.substrate, 'SUBSTRATE')
        ax.text(0.5, 0.5, f'{substrate_text}', fontsize=10, color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.6))

# --- Streamlit UI ---

st.set_page_config(page_title="Sea Slug Egg Laying Simulator", layout="wide")

st.title("Sea Slug Egg Laying Simulator")
st.markdown("""
This simulator allows you to explore the fascinating process of sea slug reproduction,
from mating and egg laying to embryonic development and hatching,
influenced by various environmental factors.
""")

# Define some sea slug species with their characteristics based on research
# Using a dictionary for easy lookup in Streamlit selectbox
SEA_SLUG_SPECIES = {
    "Pacific Sea Lemon (Peltodoris nobilis)": SeaSlug(
        species="Pacific Sea Lemon (Peltodoris nobilis)",
        egg_count_range=(100000, 2000000), # Up to 20 eggs per dot, large mass [26, 27, 7]
        egg_mass_shape="large spiral ribbon",
        coiling_direction="anticlockwise", # Typically anticlockwise from center [6, 28]
        hatching_time_range=(20, 40), # Weeks to months for veliger stage [5]
        larval_type="planktotrophic veliger", # Most species hatch as veligers [5, 12]
        is_toxic=False, # Not explicitly mentioned as toxic in snippets, but some dorids are [29]
        preferred_substrate=["rocks", "seaweed"] # Often attached to rocks or seaweed [5, 4, 30]
    ),
    "Spanish Dancer Nudibranch (Hexabranchus sanguineus)": SeaSlug(
        species="Spanish Dancer Nudibranch (Hexabranchus sanguineus)",
        egg_count_range=(500000, 5000000), # Large and numerous [27, 31, 9]
        egg_mass_shape="ruffled spiral ribbon (rose-like)",
        coiling_direction="N/A", # Not specified, but often rose-like [14]
        hatching_time_range=(10, 30), # General range for nudibranchs [5, 12]
        larval_type="planktotrophic veliger",
        is_toxic=True, # Incorporates defense toxins [11, 12, 14, 15]
        preferred_substrate=["rocks", "seaweed", "coral"] # Often laid on food source, but not specified for this species [27]
    ),
    "Vayssierea felis": SeaSlug(
        species="Vayssierea felis",
        egg_count_range=(1, 5), # As few as 1-2 eggs
        egg_mass_shape="cluster", # Not explicitly spiral for this species, often small clusters [5]
        coiling_direction="N/A",
        hatching_time_range=(30, 50), # Longer development for direct developers
        larval_type="lecithotrophic juvenile", # Few large eggs hatch as crawling slugs [5, 12]
        is_toxic=False, # Not specified
        preferred_substrate=["not specified", "algae", "sediment"]
    ),
    "Aglajid Sea Slug (e.g., Spotted Aglajid)": SeaSlug(
        species="Aglajid Sea Slug",
        egg_count_range=(1000, 100000), # Variable, but can be numerous [32]
        egg_mass_shape="coil or tube-like mass",
        coiling_direction="around rotating body", # Unique method [7]
        hatching_time_range=(10, 25),
        larval_type="planktotrophic veliger",
        is_toxic=False,
        preferred_substrate=["sediment"] # Anchored in sediment [7]
    )
}

# --- Sidebar for User Inputs ---
st.sidebar.header("Simulation Parameters")

selected_species_name = st.sidebar.selectbox(
    "Select Sea Slug Species:",
    list(SEA_SLUG_SPECIES.keys()),
    help="Choose the species to simulate. Different species have unique egg-laying characteristics."
)
selected_slug = SEA_SLUG_SPECIES[selected_species_name]

st.sidebar.subheader("Environmental Conditions")
temperature_celsius = st.sidebar.slider(
    "Water Temperature (°C):",
    min_value=10,
    max_value=30,
    value=20,
    step=1,
    help="Temperature significantly affects embryonic development speed. Warmer water generally accelerates hatching."
)

water_flow_rate = st.sidebar.slider(
    "Water Flow Rate (0.0 - 1.0, 1.0 = high flow):",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1,
    help="Water flow influences oxygen diffusion to the egg mass. Higher flow improves oxygen supply. [16, 23, 33]"
)

substrate_options = ["rock", "seaweed", "sediment", "coral", "aquarium glass", "not specified"]
default_substrate_index = 0
if selected_slug.preferred_substrate:
    for substrate in selected_slug.preferred_substrate:
        if substrate in substrate_options:
            default_substrate_index = substrate_options.index(substrate)
            break

selected_substrate = st.sidebar.selectbox(
    "Substrate for Egg Laying:",
    substrate_options,
    index=default_substrate_index,
    help="The surface where the egg mass is attached. Some species have preferences. [5, 4, 30]"
)

simulation_days = st.sidebar.number_input(
    "Simulation Duration (days):",
    min_value=10,
    max_value=100,
    value=40,
    step=5,
    help="Number of days to simulate egg mass development."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About the Simulator")
st.sidebar.markdown("""
This simulation demonstrates key biological aspects of sea slug reproduction:
- **Hermaphroditism:** Both slugs can lay eggs after mating. [2, 3, 4]
- **Egg Mass Formation:** Physical shaping by the slug's foot and mantle. [6, 10]
- **Environmental Impact:** Temperature and water flow affect development and survival.
- **Larval Strategies:** Planktotrophic (free-swimming) vs. Lecithotrophic (direct development). [5, 12, 9]
""")

# --- Main Simulation Area ---

# Initialize session state for step control
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'auto_play' not in st.session_state:
    st.session_state.auto_play = False
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = None
if 'play_speed' not in st.session_state:
    st.session_state.play_speed = 1.0

# Create visualization controls
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 2])

with col1:
    if st.button("-10"):
        st.session_state.current_step = max(0, st.session_state.current_step - 10)

with col2:
    if st.button("-1"):
        st.session_state.current_step = max(0, st.session_state.current_step - 1)

with col3:
    if st.button("+1"):
        st.session_state.current_step = min(99, st.session_state.current_step + 1)

with col4:
    if st.button("+10 f"):
        st.session_state.current_step = min(99, st.session_state.current_step + 10)

with col5:
    auto_play = st.button("Play" if not st.session_state.auto_play else "Pause")
    if auto_play:
        st.session_state.auto_play = not st.session_state.auto_play

with col6:
    progress_percent = (st.session_state.current_step + 1) / 100 * 100
    fps_text = f" • {st.session_state.play_speed*3:.1f} FPS" if st.session_state.auto_play else ""
    st.write(f"Progress: {progress_percent:.0f}% ({st.session_state.current_step + 1}/100){fps_text}")

# Speed control for autoplay
speed_col1, speed_col2 = st.columns([1, 3])
with speed_col1:
    st.write("Speed:")
with speed_col2:
    st.session_state.play_speed = st.select_slider(
        "Autoplay Speed",
        options=[0.5, 1.0, 2.0, 5.0],
        value=st.session_state.play_speed,
        format_func=lambda x: f"{x}x",
        label_visibility="collapsed"
    )

# Reset button
if st.button("Reset to Start"):
    st.session_state.current_step = 0
    st.session_state.auto_play = False

# Create visualizer if not exists or settings changed
current_settings = (selected_slug.species, selected_substrate, temperature_celsius, water_flow_rate)
if (st.session_state.visualizer is None or 
    getattr(st.session_state, 'last_settings', None) != current_settings):
    st.session_state.visualizer = EggLayingVisualizer(
        selected_slug, selected_substrate, temperature_celsius, water_flow_rate
    )
    st.session_state.last_settings = current_settings

# Display current step information
step_title, step_description = st.session_state.visualizer.get_step_info(st.session_state.current_step)

st.header(f"{step_title}")
st.write(step_description)

# Create placeholder for the visualization
viz_placeholder = st.empty()

# Auto-play functionality with proper visualization updates
if st.session_state.auto_play:
    if st.session_state.current_step < 99:
        # Update visualization immediately
        with viz_placeholder.container():
            fig = st.session_state.visualizer.create_visualization(st.session_state.current_step)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        
        # Advance to next step
        st.session_state.current_step += 1
        
        # Small delay then rerun
        time.sleep(max(0.1, 0.3 / st.session_state.play_speed))
        st.rerun()
    else:
        st.session_state.auto_play = False
        st.success("Egg laying pattern complete!")

# For non-autoplay mode, display static visualization
if not st.session_state.auto_play:
    with viz_placeholder.container():
        fig = st.session_state.visualizer.create_visualization(st.session_state.current_step)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# Progress bar with animation indicator
progress_value = (st.session_state.current_step + 1) / 100
animation_status = " ANIMATING" if st.session_state.auto_play else ""
st.progress(progress_value, text=f"Egg laying pattern formation: {int(progress_value * 100)}% complete{animation_status}")

# Display pattern statistics
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.current_step > 10:
        estimated_eggs = int((st.session_state.current_step / 100) * random.randint(selected_slug.egg_count_range[0], selected_slug.egg_count_range[1]))
        st.metric("Eggs Laid", f"{estimated_eggs:,}")

with col2:
    if st.session_state.current_step > 0:
        pattern_type = selected_slug.egg_mass_shape.title()
        st.metric("Pattern Type", pattern_type)

with col3:
    if st.session_state.current_step > 20:
        matrix_volume = round(progress_value * 2.5, 2)  # Simulated volume in mL
        st.metric("Matrix Volume", f"{matrix_volume} mL")

# Environmental impact display
if st.session_state.current_step > 50:
    st.subheader("Environmental Impact on Pattern")
    
    impact_col1, impact_col2 = st.columns(2)
    
    with impact_col1:
        temp_effect = "Accelerated" if temperature_celsius > 20 else "Slowed" if temperature_celsius < 15 else "Normal"
        st.info(f"**Temperature Effect**: {temp_effect} laying rate at {temperature_celsius}°C")
    
    with impact_col2:
        flow_effect = "Strong adhesion" if water_flow_rate > 0.7 else "Weak adhesion" if water_flow_rate < 0.3 else "Good adhesion"
        st.info(f"**Flow Effect**: {flow_effect} with current flow rate")

# Completion message and restart
if st.session_state.current_step >= 99:
    st.success("**Pattern Formation Complete!**")
    st.balloons()
    
    completion_info = f"""
    The {selected_slug.species} has successfully completed laying its egg mass in a 
    **{selected_slug.egg_mass_shape}** pattern on {selected_substrate}. 
    
    **Final Statistics:**
    - Total eggs: ~{random.randint(selected_slug.egg_count_range[0], selected_slug.egg_count_range[1]):,}
    - Pattern: {selected_slug.egg_mass_shape} with {selected_slug.coiling_direction} orientation
    - Larval type: {selected_slug.larval_type}
    - Expected hatching: {random.randint(selected_slug.hatching_time_range[0], selected_slug.hatching_time_range[1])} days
    """
    
    st.markdown(completion_info)
    
    if st.button("Start New Pattern", type="primary"):
        st.session_state.current_step = 0
        st.session_state.auto_play = False
        st.rerun()
