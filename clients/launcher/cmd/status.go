package cmd

import (
	"github.com/debasishtripathy13/Pandora/clients/launcher/internal/compose"
	"github.com/spf13/cobra"
)

var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Show Pandora service status",
	RunE: func(cmd *cobra.Command, args []string) error {
		return compose.New().Ps()
	},
}

func init() {
	rootCmd.AddCommand(statusCmd)
}
