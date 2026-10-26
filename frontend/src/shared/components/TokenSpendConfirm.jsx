import { Coins } from "lucide-react";
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useSession } from "@/shared/session/SessionProvider";
import { DemoBadge } from "@/shared/components/DemoBadge";

// The server validates and deducts the cost; this dialog only asks for confirmation.
export const TokenSpendConfirm = ({ trigger, title, description, cost, onConfirm, testId }) => {
  const { user } = useSession();
  const short = user.token_balance < cost;
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>{trigger}</AlertDialogTrigger>
      <AlertDialogContent data-testid={`${testId}-dialog`}>
        <AlertDialogHeader>
          <DemoBadge tone="purple" className="w-fit">Simulated action</DemoBadge>
          <AlertDialogTitle>{title}</AlertDialogTitle>
          <AlertDialogDescription>{description}</AlertDialogDescription>
        </AlertDialogHeader>
        <div className="flex items-center justify-between rounded-xl border border-border bg-muted/50 p-4 text-sm">
          <span className="flex items-center gap-2"><Coins className="h-4 w-4 text-gold-ink" /> Cost</span>
          <span className="font-mono font-semibold">{cost} Tokens · balance {user.token_balance}</span>
        </div>
        {short && <p className="text-sm text-warning-ink" data-testid={`${testId}-insufficient`}>Not enough Tokens. Add a demo pack in your wallet.</p>}
        <AlertDialogFooter>
          <AlertDialogCancel data-testid={`${testId}-cancel`}>Cancel</AlertDialogCancel>
          <AlertDialogAction disabled={short} onClick={onConfirm} data-testid={`${testId}-confirm`}>Spend {cost} Tokens</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};
