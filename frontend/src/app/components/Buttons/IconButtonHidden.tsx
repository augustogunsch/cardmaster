import React from 'react';
import IconButton from '@mui/material/IconButton';
import type { IconButtonProps } from '@mui/material';

const IconButtonHidden = (props: IconButtonProps): React.JSX.Element => {
  const { sx, ...other } = props;

  return (
    <IconButton
      sx={{
        '& .MuiSvgIcon-root': {
          visibility: 'hidden'
        },

        '&:hover .MuiSvgIcon-root': {
          visibility: 'visible'
        },
        ...sx
      }}
      {...other}
    />
  );
};

export default IconButtonHidden;
