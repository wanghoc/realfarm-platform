"""
CropCycle domain service and business rules.
"""

from collections.abc import Sequence

from app.modules.crop_cycles.domain.crop_cycle_model import CropCycle, CropCycleStatus


class CropCycleService:
    @staticmethod
    def validate_can_plant(plot_id: str, active_cycles_for_plot: Sequence[CropCycle]) -> None:
        """
        Business Rule: A plot MUST NOT have more than one active crop cycle at the same time.
        An active crop cycle is one that has not reached a terminal state.

        Args:
            plot_id: The plot ID to check.
            active_cycles_for_plot: List of currently non-terminal crop cycles for this plot.

        Raises:
            ValueError: If there is already an active crop cycle.
        """
        terminal_states = {
            CropCycleStatus.CLOSED,
            CropCycleStatus.FAILED,
            CropCycleStatus.CANCELLED,
        }

        for cycle in active_cycles_for_plot:
            if cycle.status not in terminal_states:
                raise ValueError(
                    f"Plot {plot_id} already has an active crop cycle (status: {cycle.status})."
                )
