import React from 'react';

import {
  CircularProgress,
  Stack
} from '@mui/material';

const Loading = (): React.JSX.Element => {
  return (
    <Stack
      justifyContent="center"
      alignItems="center"
      height="100vh"
    >
      <CircularProgress size={60} />
    </Stack>
  );
};

export default Loading;
