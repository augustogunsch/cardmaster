import React from 'react';

import {
  Avatar as MuiAvatar
} from '@mui/material';

import type {
  AvatarProps,
  SxProps,
  Theme
} from '@mui/material';

import { useAppSelector } from '../../hooks';

const stringToHslColor = (str: string, saturation: number, lightness: number): string => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }

  const hue = hash % 360;
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
};

export interface IProps extends AvatarProps {
  size?: number
}

const stringAvatar = (name: string, sx: SxProps<Theme> | undefined): object => {
  return {
    sx: {
      bgcolor: stringToHslColor(name, 30, 60),
      ...sx
    },
    children: name[0].toUpperCase(),
    alt: name
  };
};

const AvatarBase = (props: IProps): React.JSX.Element => {
  const user = useAppSelector(state => state.user);
  const { size = 40, sx, ...other } = props;

  const newSx = {
    width: size,
    height: size,
    fontSize: size / 2,
    ...sx
  };

  if (user.entity !== null) {
    return <MuiAvatar {...stringAvatar(user.entity.username, newSx)} {...other} />;
  }

  return <MuiAvatar {...props} />;
};

export default AvatarBase;
