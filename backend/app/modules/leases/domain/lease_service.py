"""
Lease domain service and business rules.
"""

from typing import Sequence

from app.modules.leases.domain.lease_model import Lease, LeaseStatus


class LeaseService:
    @staticmethod
    def validate_can_activate_lease(plot_id: str, active_leases_for_plot: Sequence[Lease]) -> None:
        """
        Business Rule: A plot MUST NOT have more than one active lease at the same time.
        
        Args:
            plot_id: The plot ID to check.
            active_leases_for_plot: List of currently active leases for this plot.
            
        Raises:
            ValueError: If there is already an active lease.
        """
        for lease in active_leases_for_plot:
            if lease.status == LeaseStatus.ACTIVE:
                raise ValueError(f"Plot {plot_id} already has an active lease.")
