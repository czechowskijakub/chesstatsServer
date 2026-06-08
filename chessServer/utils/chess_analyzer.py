import io
import chess
import chess.engine
import chess.pgn

class ChessAnalyzer:
    @staticmethod
    def get_accuracies(pgn: str):
        stockfish_path = "/usr/local/bin/stockfish"
        stockfish = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        stockfish.configure({
            "Threads": 1,
            "Hash": 64,
        })
        
        game = chess.pgn.read_game(io.StringIO(pgn))
        if not game:
            stockfish.quit()
            return {"white": 0.0, "black": 0.0}
            
        board = game.board()
        
        white_loss = 0
        white_moves = 0
        
        black_loss = 0
        black_moves = 0
        
        for move in game.mainline_moves():
            if board.is_game_over():
                break
                
            current_turn = board.turn
                
            analysis_before = stockfish.analyse(board, chess.engine.Limit(time=0.1))
            score_before = analysis_before["score"].pov(current_turn).score(mate_score=400)
            
            board.push(move)
            
            analysis_after = stockfish.analyse(board, chess.engine.Limit(time=0.1))
            score_after = analysis_after["score"].pov(current_turn).score(mate_score=400)
            
            loss = max(0, score_before - score_after)
            
            if current_turn == chess.WHITE:
                white_loss += loss
                white_moves += 1
            else:
                black_loss += loss
                black_moves += 1
            
        stockfish.quit()
        
        avg_white_loss = white_loss / white_moves if white_moves > 0 else 0
        avg_black_loss = black_loss / black_moves if black_moves > 0 else 0
            
        white_accuracy = max(0, min(100, 100 - (avg_white_loss * 0.4)))
        black_accuracy = max(0, min(100, 100 - (avg_black_loss * 0.4)))
        
        return {
            "white": round(white_accuracy, 2),
            "black": round(black_accuracy, 2)
        }