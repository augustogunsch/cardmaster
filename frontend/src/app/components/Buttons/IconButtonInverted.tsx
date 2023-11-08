import React from 'react';
import { IconButton } from '@mui/material';
import type { IconButtonProps } from '@mui/material';

const IconButtonInverted = (props: IconButtonProps): React.JSX.Element => {
  const { color, sx, ...other } = props;

  return (
    <IconButton
      sx={{
        backgroundColor: `${color}.main`,
        color: `${color}.contrastText`,
        '&:hover': {
          backgroundColor: `${color}.light`
        },
        ...sx
      }}
      {...other}
    />
  );
};

export default IconButtonInverted;
