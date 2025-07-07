import { Hero } from './components/layout/Hero';
import { Features } from './components/layout/Features';
import { HowItWorks } from './components/layout/HowItWorks';

export default function HomePage() {
  return (
    <div className="space-y-20">
      <Hero />
      <Features />
      <HowItWorks />
    </div>
  );
}