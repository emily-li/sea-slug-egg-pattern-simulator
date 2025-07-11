import streamlit as st
import random

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

        num_eggs = random.randint(self.egg_count_range, self.egg_count_range[1])
        
        # Simulate the physical shaping of the egg mass
        st.write(f"The {self.species} begins extruding a continuous stream of fertilized eggs and gelatinous matrix from its genital aperture. [7, 8, 9]")
        st.write(f"Using its muscular foot and mantle edge, the slug actively manipulates and presses the material against the substrate, sculpting it into a **{self.egg_mass_shape}** with a **{self.coiling_direction}** coiling direction. [6, 10]")
        
        # Determine hatching time, influenced by temperature
        base_hatching_days = random.randint(self.hatching_time_range, self.hatching_time_range[1])
        
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

# --- Streamlit UI ---

st.set_page_config(page_title="Sea Slug Egg Laying Simulator", layout="wide")

st.title("🌊 Sea Slug Egg Laying Simulator")
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
selected_substrate = st.sidebar.selectbox(
    "Substrate for Egg Laying:",
    substrate_options,
    index=substrate_options.index(selected_slug.preferred_substrate) if selected_slug.preferred_substrate and selected_slug.preferred_substrate in substrate_options else 0,
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
if st.button("Start Simulation"):
    st.header("Simulation Results")
    
    # Create two instances of the selected slug for mating
    slug1 = selected_slug
    slug2 = selected_slug # For simplicity, assuming two of the same species mate

    st.subheader("Mating Event")
    if slug1.mate(slug2):
        st.subheader("Egg Laying Process")
        egg_mass1 = slug1.lay_eggs(selected_substrate, temperature_celsius, water_flow_rate)
        egg_mass2 = slug2.lay_eggs(selected_substrate, temperature_celsius, water_flow_rate)

        egg_masses = [egg_mass1, egg_mass2]

        st.subheader("Embryonic Development Over Time")
        for day in range(1, simulation_days + 1):
            for i, em in enumerate(egg_masses):
                with st.expander(f"Details for Egg Mass {i+1} on Day {day}"):
                    if not em.hatched:
                        em.simulate_development(day, temperature_celsius, water_flow_rate)
                    else:
                        st.info(f"Egg Mass {i+1} has already hatched.")
            
            # Stop if all masses have hatched
            if all(em.hatched for em in egg_masses):
                st.success("\nAll egg masses have hatched. Simulation complete.")
                break
        else:
            st.info("\nSimulation finished. Not all egg masses may have hatched yet within the specified duration.")
    else:
        st.error("Mating was unsuccessful. No eggs laid.")
