import React from 'react';

import {
  Link,
  Stack,
  Typography
} from '@mui/material';
import { GitHub } from '@mui/icons-material';

const Footer = (): React.JSX.Element => {
  return (
    <Stack
      direction="row"
      sx={{
        backgroundColor: 'primary.dark',
        color: 'primary.contrastText',
        padding: 2
      }}
      justifyContent="space-between"
    >
      <Typography
        variant="body2"
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}
      >
        <GitHub />
        <Link
          color="inherit"
          href="https://github.com/augustogunsch/cardmaster"
          target="_blank"
        >
          Repository
        </Link>
      </Typography>
      <Typography
        variant="body2"
      >
        made by <Link
          color="inherit"
          href="https://augustogunsch.com"
          target="_blank"
        >
          Augusto Gunsch
        </Link>
      </Typography>
    </Stack>
  );
};

export default Footer;
