import React from 'react';
import AvatarBase from './AvatarBase';
import { Box } from '@mui/material';
import { CameraAlt } from '@mui/icons-material';
import IconButtonHidden from '../Buttons/IconButtonHidden';

export interface IProps {
  size?: number
  onClick: () => void
}

const AvatarEdit = ({ size = 40, onClick }: IProps): React.JSX.Element => {
  return (
    <Box
      sx={{
        position: 'relative',
        width: size,
        height: size
      }}
    >
      <IconButtonHidden
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          zIndex: 1,
          width: size,
          height: size
        }}
        onClick={onClick}
      >
        <CameraAlt
          sx={{
            width: size / 2,
            height: size / 2
          }}
        />
      </IconButtonHidden>
      <AvatarBase
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          zIndex: -1
        }}
        size={size}
      />
    </Box>
  );
};

export default AvatarEdit;
