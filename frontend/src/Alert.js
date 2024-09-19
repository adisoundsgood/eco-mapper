import React from 'react';

const Alert = ({ variant = 'info', title, children }) => {
  const getColorClasses = () => {
    switch (variant) {
      case 'destructive':
        return 'bg-red-100 border-red-400 text-red-700';
      case 'warning':
        return 'bg-yellow-100 border-yellow-400 text-yellow-700';
      case 'success':
        return 'bg-green-100 border-green-400 text-green-700';
      default:
        return 'bg-blue-100 border-blue-400 text-blue-700';
    }
  };

  return (
    <div className={`border-l-4 p-4 ${getColorClasses()}`} role="alert">
      {title && <p className="font-bold">{title}</p>}
      <p>{children}</p>
    </div>
  );
};

export default Alert;