package cmd

import (
	"github.com/debasishtripathy13/Pandora/clients/launcher/internal/compose"
	"github.com/debasishtripathy13/Pandora/clients/launcher/internal/ui"
	"github.com/spf13/cobra"
)

var stopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Stop all Pandora services",
	RunE: func(cmd *cobra.Command, args []string) error {
		c := compose.New()
		ui.Info("Stopping Pandora services...")
		c.RemoveOrphanedCLI()
		// Clear legacy root-level scratch/session buffers before tearing the
		// stack down. Current runs keep these under engagement workspaces.
		c.CleanScratch()
		if err := c.Down(); err != nil {
			return err
		}
		ui.Success("All services stopped")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(stopCmd)
}
