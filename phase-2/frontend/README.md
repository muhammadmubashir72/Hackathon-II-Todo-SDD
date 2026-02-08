# TaskFlow - Todo Management Application

TaskFlow is a modern, full-stack web application for managing tasks and improving productivity. Built with Next.js, it features a beautiful UI with 3D animations, responsive design, and complete authentication flow.

## Features

- **Beautiful UI/UX**: Modern design with gradients, animations, and dark mode support
- **3D Graphics**: Interactive 3D floating shapes using Three.js and React Three Fiber
- **Authentication**: Complete login/register flow with mock authentication
- **Task Management**: Create, update, and manage tasks with local storage persistence
- **Responsive Design**: Works on all device sizes
- **Dark Mode**: Toggle between light and dark themes

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom-built with Tailwind
- **3D Graphics**: Three.js, React Three Fiber, React Three Drei
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **State Management**: React Hooks
- **Theming**: next-themes

## Project Structure

```
phase-2/frontend/
├── app/                    # Next.js App Router pages
│   ├── login/             # Login page
│   ├── register/          # Registration page  
│   ├── dashboard/         # Main dashboard with tasks
│   ├── tasks/             # Task detail pages
│   └── globals.css        # Global styles
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── 3d/           # 3D graphics components
│   │   ├── auth/         # Authentication components
│   │   ├── common/       # Common UI elements
│   │   ├── tasks/        # Task-specific components
│   │   └── ui/           # Base UI components
│   ├── context/          # React context providers
│   ├── services/         # Business logic and API services
│   └── utils/            # Utility functions
```

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Lint the codebase

## Key Functionality

### Authentication Flow
- Users can register with name, email, and password
- Secure login with credential validation
- Session management with mock authentication service
- Protected routes that redirect unauthenticated users

### Task Management
- Create new tasks with title and description
- Mark tasks as complete/incomplete
- Delete tasks
- View pending/completed tasks
- Data persisted in browser's local storage

### UI Features
- Smooth animations using Framer Motion
- Dark/light theme toggle
- Responsive layout for all screen sizes
- Interactive 3D background on home page
- Gradient designs and modern UI elements

## Custom Components

### 3D Floating Shapes (`src/components/3d/FloatingShapes.tsx`)
- Interactive 3D shapes using React Three Fiber
- Floating animation effect
- Environment lighting and controls

### Animated Components (`src/components/ui/AnimatedComponents.tsx`)
- Section animations with fade-in effects
- Card hover animations
- Staggered entrance animations

### Theme Toggle (`src/components/ui/ThemeToggle.tsx`)
- Switch between light and dark modes
- Persists user preference
- Uses next-themes for theme management

## Authentication Service

The `AuthService` in `src/services/auth_service.ts` provides:
- Authentication state management
- Login/logout functionality
- Token storage in localStorage
- Authentication status checking

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.