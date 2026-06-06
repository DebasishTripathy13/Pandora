import React from "react";
import { Text, Box } from "ink";

// ── Banner: red PANDORA wordmark, no logo art ──

export const Banner = React.memo(function Banner() {
  return (
    <Box marginTop={1} marginBottom={1}>
      <Text color="red" bold>
        {"P A N D O R A"}
      </Text>
    </Box>
  );
});
