import React, { useState } from 'react';
import IconButton from '@mui/material/IconButton';
import type { IconButtonProps } from '@mui/material/IconButton';

export interface IProps extends IconButtonProps {
  iconA: React.ReactNode
  iconB: React.ReactNode
}

const IconButtonAlternate = (props: IProps): React.JSX.Element => {
  const { iconA, iconB, disabled, onClick, children, ...restProps } = props;
  const [showA, setShowA] = useState(true);

  const onClickDecorated = (e: React.MouseEvent<HTMLButtonElement>): void => {
    if (onClick !== undefined) {
      onClick(e);
    }

    setShowA(false);
    setTimeout(() => {
      setShowA(true);
    }, 1500);
  };

  return (
    <IconButton
      disabled={disabled ?? !showA}
      onClick={onClickDecorated}
      {...restProps}
    >
      {showA && iconA}
      {!showA && iconB}
    </IconButton>
  );
};

export default IconButtonAlternate;
