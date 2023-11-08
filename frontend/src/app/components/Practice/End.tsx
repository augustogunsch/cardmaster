import React from 'react';

import {
  Button,
  Typography,
  Stack
} from '@mui/material';

export interface IProps {
  handleClose: () => void
}

const End = ({ handleClose }: IProps): React.JSX.Element => {
  return (
    <Stack
      alignItems="center"
      padding={2}
      gap={4}
      maxWidth="sm"
    >
      <Typography>
        Congratulations! You finished this review session.
      </Typography>
      <Button
        onClick={handleClose}
        variant="contained"
      >
        Leave
      </Button>
    </Stack>
  );
};

export default End;
